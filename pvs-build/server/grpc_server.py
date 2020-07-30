from concurrent import futures
import logging
import grpc
import json, os, re, ast
import unicodedata
import sys
import socket
import thread

from protobuffs import p4runtime_pb2 as p4runtime_pb2
from protobuffs import p4runtime_pb2_grpc as p4runtime_pb2_grpc

from protobuffs.code_pb2 import *
from protobuffs.auth_pb2 import *

from utils.RPC_mgmt import *
from utils.PMA_mgmt import *
from server.connections import *
from sniffer import Sniffer
from config import ServerConfig
from examples.virtual_switches.LoadVSwitch import *
from utils.Auth import *
from server.connections.ConnectionArray import *

class PacketInStruct():
    def __init__(self):
        self.packetInResponse = p4runtime_pb2.StreamMessageResponse()
        self.packetInResponse.packet.payload = " "
        self.metadata = self.packetInResponse.packet.metadata.add()
        self.metadata.metadata_id = 0
        self.metadata.value = " "

class P4Runtime(p4runtime_pb2_grpc.P4RuntimeServicer):

    def __init__(self):
        self.host = ServerConfig.HOST
        self.server_port = ServerConfig.SERVER_PORT
        self.device_id = 0

        with open(ServerConfig.SERVER_CERTIFICATE, "rb") as file:
            trusted_certs = file.read()

        self.credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        self.channel = grpc.secure_channel("{}:{}".format(self.host, self.server_port), self.credentials)
        self.stub = p4runtime_pb2_grpc.P4RuntimeStub(self.channel)

    def SetForwardingPipelineConfig(self, request, context):
        return RPC_mgmt.process_setPipe(request, context)

    def GetForwardingPipelineConfig(self, request, context):
        return RPC_mgmt.process_getPipe(request, context)

    def StreamChannel(self, request_iterator, context):
        response = RPC_mgmt.process_streamChannel(self, request_iterator, context)
        return response

    def Write(self, request, context):
        return RPC_mgmt.process_write_request(self, request, context)

    def Read(self, request, context):
        return RPC_mgmt.process_read_request(request, context)

    # CLI methods.
    def CLI_PMA_init_database():
        return PMA_mgmt.init_database()

    def CLI_PMA_load_switch_data(switch_name, dir_path, switch_id, switch_dat_file, table_defines_file):
        return PMA_mgmt.load_switch_data(switch_name, dir_path, switch_id, switch_dat_file, table_defines_file)

    def CLI_PMA_load_switch_modules(switch_name, dir_path, switch_id):
        return PMA_mgmt.load_switch_modules(switch_name, dir_path, switch_id)

    def CLI_PMA_load_reg_data(switch_id, extern_defines_file):
        return PMA_mgmt.load_reg_data(switch_id, extern_defines_file)

    def CLI_PMA_load_libsume_module(lib_path):
        return PMA_mgmt.load_libsume_module(lib_path)

def sniffer_thread():
    sniffer_instance = Sniffer(ServerConfig.PACKETIN_IFACE, 1500)

    newPacketIn = PacketInStruct()

    print "Sniffer Thread Started"

    while True:
        pack_data = sniffer_instance.recv_packet_in()
        if pack_data is not False and pack_data[0] < 4: #TODO: Remover "and pack_data[0] < 4", esta aqui para nao capturar outros pacotes na interface de teste
            newPacketIn.packetInResponse = p4runtime_pb2.StreamMessageResponse()
            newPacketIn.packetInResponse.packet.payload = pack_data[2]
            newPacketIn.metadata = newPacketIn.packetInResponse.packet.metadata.add()
            newPacketIn.metadata.metadata_id = pack_data[0]
            newPacketIn.metadata.value = pack_data[1]

            print "Packet-in: interface => server %.9f" % time.time()
            ConnectionArray.sendPacketInToBuffer(newPacketIn)

if __name__ == "__main__":
    logging.basicConfig()

    # This line is required only if running pvs_control_engine for demo purposes.
    LoadVSwitch.load_switches()

    Auth.loadDbMemory()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    p4runtime_instance = P4Runtime()
    p4runtime_pb2_grpc.add_P4RuntimeServicer_to_server(p4runtime_instance, server)

    with open(ServerConfig.SERVER_KEY, "rb") as file:
        private_key = file.read()
    with open(ServerConfig.SERVER_CERTIFICATE, "rb") as file:
        certificate_chain = file.read()

    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))
    # server.add_insecure_port('localhost:50052')
    server.add_secure_port("[::]:{}".format(p4runtime_instance.server_port), server_credentials)
    server.start()
    print "PvS P4Runtime server running @ grpcs://{}:{}".format(p4runtime_instance.host, p4runtime_instance.server_port)

    thread.start_new_thread(sniffer_thread, ())

    server.wait_for_termination()

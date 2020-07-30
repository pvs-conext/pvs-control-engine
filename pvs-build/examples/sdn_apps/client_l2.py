import grpc
import struct

from protobuffs import p4runtime_pb2 as p4runtime_pb2
from protobuffs import p4runtime_pb2_grpc as p4runtime_pb2_grpc
from protobuffs import auth_pb2 as auth_pb2

from config import ServerConfig

from scapy.all import *
from binascii import hexlify

DMAC = 0
eth_dict = {
    "00:15:4d:13:61:49": "0b00000001",
    "00:15:4d:13:61:07": "0b00000100",
    "00:15:4d:13:61:4a": "0b00010000",
    "00:15:4d:13:61:08": "0b01000000",
    }

dev_id = 1

"""
Switch identifiers are defined in the 'example_virtual_switches.LoadVSwitch' class.
Note that the 'l2' switch currently has id 1.
"""
class P4RuntimeClient():

    def __init__(self):
        # Configure the host and the port to which the client should connect to.
        self.host = ServerConfig.HOST
        self.server_port = ServerConfig.SERVER_PORT

        with open(ServerConfig.SERVER_CERTIFICATE, "rb") as file:
            trusted_certs = file.read()

        # Instantiate a communication channel and bind the client to the server.
        self.credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        self.channel = grpc.secure_channel("{}:{}".format(self.host, self.server_port), self.credentials)
        self.stub = p4runtime_pb2_grpc.P4RuntimeStub(self.channel)

        self.streamChannelRequest = p4runtime_pb2.StreamMessageRequest()
        self.sendRequest = True

    def StreamChannel(self):
        global dev_id

        # Prepare an authentication request.
        login = auth_pb2.Auth()
        login.user_name = "admin"
        login.passwd = "admin"
        self.streamChannelRequest.other.Pack(login)

        def request():
            while True:
                if self.sendRequest:
                    self.sendRequest = False
                    yield self.streamChannelRequest
                else:
                    yield p4runtime_pb2.StreamMessageRequest()

        return self.stub.StreamChannel(request())

    # Update type can be INSERT, MODIFY or DELETE.
    def WriteTableEntry(self, update_type, table, eth_dst):
        global dev_id
        request = p4runtime_pb2.WriteRequest()
        request.device_id = dev_id
        request.election_id.low = 1

        update = request.updates.add()
        update.type = update_type
        update.entity.table_entry.table_id = table
        update.entity.table_entry.is_default_action = 1
        update.entity.table_entry.action.action.action_id = 1

        matches = update.entity.table_entry.match.add()
        matches.field_id = 1
        matches.exact.value = bytes(eth_dst)

        act = update.entity.table_entry.action.action.params.add()
        act.param_id = 2
        act.value = bytes(eth_dict[eth_dst])

        ServerConfig.print_debug("Sending table write request to server:")
        ServerConfig.print_debug(request)
        try:
            self.stub.Write(request)
        except grpc.RpcError as error:
            ServerConfig.print_debug("An error ocurred during a 'write' execution!")
            ServerConfig.print_debug("{}: {}".format(error.code().name, error.details()))

        return

    def ReadTableEntry(self, table, eth_dst):
        global dev_id
        request = p4runtime_pb2.ReadRequest()
        request.device_id = dev_id

        entity = request.entities.add()
        entity.table_entry.table_id = table
        matches = entity.table_entry.match.add()
        matches.field_id = 1
        matches.exact.value = bytes(eth_dst)

        ServerConfig.print_debug("Sending table read request to server:")
        ServerConfig.print_debug(request)
        try:
            for response in self.stub.Read(request):
                ServerConfig.print_debug("Table read response received from server:")
                ServerConfig.print_debug(response)
        except grpc.RpcError as error:
            ServerConfig.print_debug("An error occured during a 'read' execution!")
            ServerConfig.print_debug("{}: {}\n".format(error.code().name, error.details()))

        return

def main():
    global dev_id

    host = ServerConfig.HOST
    server_port = ServerConfig.SERVER_PORT
    with open(ServerConfig.SERVER_CERTIFICATE, "rb") as file:
            trusted_certs = file.read()

    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel("{}:{}".format(host, server_port), credentials)
    client = P4RuntimeClient()

    streamC = client.StreamChannel()
    while True:
        try:
            packet = next(streamC)

            # we will only process packet-ins from l2 (check device id)
            if packet.HasField("packet") and packet.packet.metadata[0].metadata_id == dev_id:
                print "Packet-in: server => l2 controller %.9f" % time.time()
                # Print packet info.
                ServerConfig.print_debug("Received packet from switch ID {} input port {}".format(packet.packet.metadata[0].metadata_id, struct.unpack("Q", packet.packet.metadata[0].value)[0]))
                # print "Payload: {}".format(hexlify(packet.packet.payload))
		#print packet.packet

                # Extract packet.
                pkt = Ether(_pkt=packet.packet.payload)
                eth_src = pkt.getlayer(Ether).src
                eth_dst = pkt.getlayer(Ether).dst
                ether_type = pkt.getlayer(Ether).type
                ServerConfig.print_debug("Received Ethernet frame {} => {} type_hex {}".format(eth_src, eth_dst, hex(ether_type)))

                # Call to insert the entry into the table.
                #client.WriteTableEntry(p4runtime_pb2.Update.INSERT, DMAC, eth_dst)

                # # Call to read the entry from the table.
                # client.ReadTableEntry(DMAC, eth_dst)

                # Packet out.
                client.streamChannelRequest = p4runtime_pb2.StreamMessageRequest()
                client.streamChannelRequest.packet.payload = packet.packet.payload
                metadata = client.streamChannelRequest.packet.metadata.add()
                metadata.metadata_id = packet.packet.metadata[0].metadata_id
                metadata.value = struct.pack("B", 1)
                client.sendRequest = True
                print "Packet-out: l2 controller => server %.9f" % time.time()

            if packet.HasField("other"):
                if packet.other.value == "\n\014Auth success":

                    ServerConfig.print_debug("Received authentication response from server:")
                    ServerConfig.print_debug(packet)

                    # Prepare an arbitration request.
                    client.streamChannelRequest = p4runtime_pb2.StreamMessageRequest()
                    client.streamChannelRequest.arbitration.device_id = dev_id
                    client.streamChannelRequest.arbitration.role.id = 1
                    client.sendRequest = True

            if packet.HasField("arbitration"):
                ServerConfig.print_debug("Received master arbitration response from server:")
                ServerConfig.print_debug(packet)
                pass

        except IndexError:
            continue

if __name__ == "__main__":
    main()

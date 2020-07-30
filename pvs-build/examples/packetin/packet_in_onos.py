from scapy.all import *
import sys

class Metadata(Packet):

	name = "MetadataPacket"
	fields_desc = [XByteField("metadata_id",1),
		           XByteField("port", 1)]

metadata = Metadata(metadata_id=1, port=1)
eth = Ether()
tcp = TCP(dport=53, flags='S')
ip = IP(frag=0, proto="tcp")
payload = Raw(load="Payload")

packet = metadata/eth/tcp/ip/payload
sendp(packet)

# Macro definitions used by the server and
# both clients.

# Create 'enp0s3' alias: sudo ifconfig enp0s3:0 <ip> up
# For example, if the interface has ip 10.0.2.15, use 10.0.2.16 for the alias.

HOST = "localhost"
SERVER_PORT = 50051
SERVER_CERTIFICATE = "tls_certificates/server.crt"
SERVER_KEY = "tls_certificates/server.key"
#PACKETIN_IFACE = "nf3" # (nf3) if where switches send packet-in to controller
#PACKETOUT_IFACE = "nf2" # (nf2) if where controller sends packet-out to switches
PACKETIN_IFACE = "enp0s3" # (nf3) if where switches send packet-in to controller
PACKETOUT_IFACE = "enp0s3" # (nf2) if where controller sends packet-out to switches

DEBUG_MODE = True

def print_debug(str):
    if DEBUG_MODE:
        print str

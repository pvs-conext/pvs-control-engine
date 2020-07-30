# This module keeps track of every connection made since
# the server's reset. The key contained inside every RPC
# context is used to identify unique connections.

# TODO: detect new connections before authentication.
# TODO: detect and delete unused connections.

import grpc
from utils.Auth import *
from utils.SwitchConf import *

from binascii import hexlify

from Connection import *
from model.objects.SwitchObject import *
from model.objects.SwitchTableObject import *
from model.objects.User import *

from config import PermEnum
from config import ServerConfig

_connections = {}

class ConnectionArray():

    @staticmethod
    def sendPacketInToBuffer(packet_in):
        global _connections
        switch_id = packet_in.metadata.metadata_id
        for connection in _connections.values():
            if Auth.hasPermissionForSwitch(connection.user.user_id, switch_id, PermEnum.PACKET_EVENT | PermEnum.DEVICE_EVENT):
                if len(connection.packet_in_buffer) == 0 or connection.packet_in_buffer[len(connection.packet_in_buffer) - 1] != packet_in:
                    connection.packet_in_buffer.append(packet_in)
        return

    @staticmethod
    def getPacketInFromBuffer(user_name):
        global _connections
        for connection in _connections.values():
	    vls = _connections.values()
	    vls_iterator = iter(vls)
	    first_value = next(vls_iterator)
            if first_value.user.user_name == user_name:
                if len(first_value.packet_in_buffer) > 0:
                    packet_in = first_value.packet_in_buffer[0]
                    first_value.packet_in_buffer.pop(0)
                    return packet_in
        return False

    @staticmethod
    def add(peer_key, user_name):
        global _connections
        if peer_key not in _connections:
            user = Auth.getUserByName(user_name)
            _connections[peer_key] = Connection(user)
            ServerConfig.print_debug("Added {} (user id {}) to ConnectionArray".format(_connections[peer_key].user.user_name, _connections[peer_key].user.user_id))
        return

    @staticmethod
    def remove(peer_key):
        global _connections
        if peer_key in _connections:
            ServerConfig.print_debug("Removed {} (user id {}) from ConnectionArray".format(_connections[peer_key].user.user_name, _connections[peer_key].user.user_id))
            del _connections[peer_key]
        return

    @staticmethod
    def authenticate(peer_key):
        global _connections
        _connections[peer_key].state = Connection.CLIENT_AUTHENTICATED
        ServerConfig.print_debug("Authenticated {} (user id {})".format(_connections[peer_key].user.user_name, _connections[peer_key].user.user_id))
        return

    @staticmethod
    def getState(peer_key):
        global _connections
        return _connections[peer_key].state

    @staticmethod
    def getUsername(peer_key):
        global _connections
        try:
            name = _connections[peer_key].user.user_name
            return name
        except KeyError:
            return "NO_USER"

    @staticmethod
    def isConnected(peer_key):
        global _connections
        return (_connections[peer_key].state == Connection.CLIENT_CONNECTED)

    @staticmethod
    def isAuthenticated(peer_key):
        global _connections
        return (_connections[peer_key].state == Connection.CLIENT_AUTHENTICATED)

    @staticmethod
    def verifyPermission(context, target, permission):
        global _connections
        user_id = _connections[context.peer()].user.user_id

        # Process permissions that apply to a switch.
        if isinstance(target, SwitchObject):
            return Auth.hasPermissionForSwitch(user_id, target.switch_id, permission)

        # Process permissions that apply to a switch table.
        elif isinstance(target, SwitchTableObject):
            return True

        else:
            return False

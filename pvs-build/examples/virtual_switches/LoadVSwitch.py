import os

from utils.PMA_mgmt import *
from config.PermEnum import *

class LoadVSwitch():

	@staticmethod
	def load_switches():
		PMA_mgmt.init_database()
		PMA_mgmt.load_libsume_module("platform_api/lib/hwtestlib/libsume.so")

		Auth.addUser("admin", "admin")
		Auth.addUser("will", "191297")
		Auth.addUser("ivan", "220998")

		# VSWITCH = os.environ["PVS_VSWITCH"]
		VSWITCH = "l2_router_int"

		# TODO: Auto-generated switch id?
		switch_id = 1;

		if "l2" in VSWITCH:
			print "Loading l2 switch (id: {}), modules @ platform_api/lib/l2/, switch_data @ platform_api/lib/l2/switch_info.dat".format(switch_id)
			PMA_mgmt.load_switch_data("l2", "platform_api/lib/l2/", switch_id, "platform_api/lib/l2/switch_info.dat", "platform_api/lib/l2/table_defines.json")
			PMA_mgmt.load_switch_modules("l2", "platform_api/lib/l2/", switch_id)
			PMA_mgmt.load_reg_data("l2", switch_id, "platform_api/lib/l2/extern_defines.json")

			Auth.addPermission("admin", "l2", DEVICE_EVENT | PACKET_EVENT | PACKET_READ | PACKET_WRITE | DEVICE_WRITE | FLOWRULE_WRITE | RESOURCE_WRITE | DEVICE_READ | FLOWRULE_READ | RESOURCE_READ)

			Auth.addPermission("ivan", "l2", DEVICE_EVENT | PACKET_EVENT | FLOWRULE_WRITE | FLOWRULE_READ | DEVICE_READ | RESOURCE_READ)

			switch_id += 1

		if "router" in VSWITCH:
			print "Loading router switch (id: {}), modules @ platform_api/lib/router/, switch_data @ platform_api/lib/router/switch_info.dat".format(switch_id)
			PMA_mgmt.load_switch_data("router", "platform_api/lib/router/", switch_id, "platform_api/lib/router/switch_info.dat", "platform_api/lib/router/table_defines.json")
			PMA_mgmt.load_switch_modules("router", "platform_api/lib/router/", switch_id)
			PMA_mgmt.load_reg_data("router", switch_id, "platform_api/lib/router/extern_defines.json")

			Auth.addPermission("admin", "router", DEVICE_EVENT | PACKET_EVENT | DEVICE_WRITE | FLOWRULE_WRITE | RESOURCE_WRITE | DEVICE_READ | FLOWRULE_READ | RESOURCE_READ)

			switch_id += 1

		if "int" in VSWITCH:
			print "Loading int switch (id: {}), modules @ platform_api/lib/int/, switch_data @ platform_api/lib/int/switch_info.dat".format(switch_id)
			PMA_mgmt.load_switch_data("int", "platform_api/lib/int/", switch_id, "platform_api/lib/int/switch_info.dat", "platform_api/lib/int/table_defines.json")
			PMA_mgmt.load_switch_modules("int", "platform_api/lib/int/", switch_id)
			PMA_mgmt.load_reg_data("int", switch_id, "platform_api/lib/int/extern_defines.json")

			Auth.addPermission("admin", "int", DEVICE_EVENT | PACKET_EVENT | DEVICE_WRITE | FLOWRULE_WRITE | RESOURCE_WRITE | DEVICE_READ | FLOWRULE_READ | RESOURCE_READ)

			switch_id += 1

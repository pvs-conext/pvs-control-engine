# Running Control Engine with ONOS

The PvS Control Engine also supports the use of ONOS, allowing the use of SDN applications. To achieve that integration, please follow the steps bellow:


## ONOS Installation Instructions

Follow the guidelines of the ONOS official wiki, in the [developer section].

To run the ONOS Security mode, it's important to install a version that has support. In the ONOS 2.x versions, might not work as their warning says:
 > In ONOS 2.x, this mode is deprecated as it does not work without additional effort in order to support Apache Karaf 4.x.

## Integrating both systems

On the terminal 1, we're going to build and execute ONOS.
```sh
$ bazel build onos
$ bazel run onos-local -- clean debug
```
If the environment variables are set in your computer, you may also use the "ok" command, which is an alias to run ONOS locally.

On the terminal 2, we're going to enter ONOS CLI to activate drivers and applications.
 ```sh
$ ssh -p 8101 karaf@localhost
```
Since we don't need lldp app, we will deactivate it. Also, the bmv2 driver needs to be started.
After you're logged in, run the following commands:
```
onos> app deactivate org.onosproject.lldpprovider
onos> app activate org.onosproject.drivers.bmv2
```

You should see the following message on the ONOS log:

```
Deactivated org.onosproject.lldpproject
Application org.onosproject.drivers.bmv2 has been activated
```

You can see all the applications and drivers that are enabled in ONOS, by using the command:
```
onos> apps -s -a
```
Make sure that the bmv2 driver is enabled, and also p4runtime drivers, such as bellow:
```
*   3 org.onosproject.yang                 2.4.0.SNAPSHOT YANG Compiler and Runtime
*   4 org.onosproject.config               2.4.0.SNAPSHOT Dynamic Configuration
*   6 org.onosproject.faultmanagement      2.4.0.SNAPSHOT Fault Management
*   8 org.onosproject.optical-model        2.4.0.SNAPSHOT Optical Network Model
*  10 org.onosproject.netconf              2.4.0.SNAPSHOT NETCONF Provider
*  11 org.onosproject.restsb               2.4.0.SNAPSHOT REST Provider
*  12 org.onosproject.models.tapi          2.4.0.SNAPSHOT ONF Transport API YANG Models
*  13 org.onosproject.models.ietf          2.4.0.SNAPSHOT IETF YANG Models
*  14 org.onosproject.models.openconfig    2.4.0.SNAPSHOT OpenConfig YANG Models
*  15 org.onosproject.models.openconfig-infinera 2.4.0.SNAPSHOT OpenConfig Infinera XT3300 YANG Models
*  16 org.onosproject.models.openconfig-odtn 2.4.0.SNAPSHOT OpenConfig RD v0.3 YANG Models
*  17 org.onosproject.odtn-api             2.4.0.SNAPSHOT ODTN API & Utilities Application
*  18 org.onosproject.drivers.netconf      2.4.0.SNAPSHOT Generic NETCONF Drivers
*  19 org.onosproject.drivers              2.4.0.SNAPSHOT Default Drivers
*  20 org.onosproject.drivers.optical      2.4.0.SNAPSHOT Basic Optical Drivers
*  21 org.onosproject.protocols.grpc       2.4.0.SNAPSHOT gRPC Protocol Subsystem
*  22 org.onosproject.protocols.gnmi       2.4.0.SNAPSHOT gNMI Protocol Subsystem
*  23 org.onosproject.generaldeviceprovider 2.4.0.SNAPSHOT General Device Provider
*  24 org.onosproject.drivers.gnmi         2.4.0.SNAPSHOT gNMI Drivers
*  25 org.onosproject.drivers.odtn-driver  2.4.0.SNAPSHOT ODTN Driver
*  35 org.onosproject.protocols.gnoi       2.4.0.SNAPSHOT gNOI Protocol Subsystem
*  36 org.onosproject.drivers.gnoi         2.4.0.SNAPSHOT gNOI Drivers
*  37 org.onosproject.protocols.p4runtime  2.4.0.SNAPSHOT P4Runtime Protocol Subsystem
*  38 org.onosproject.p4runtime            2.4.0.SNAPSHOT P4Runtime Provider
*  39 org.onosproject.drivers.p4runtime    2.4.0.SNAPSHOT P4Runtime Drivers
*  40 org.onosproject.pipelines.basic      2.4.0.SNAPSHOT Basic Pipelines
*  41 org.onosproject.drivers.stratum      2.4.0.SNAPSHOT Stratum Drivers
*  42 org.onosproject.drivers.bmv2         2.4.0.SNAPSHOT BMv2 Drivers
* 114 org.onosproject.gui2                 2.4.0.SNAPSHOT ONOS GUI2
```

Now, we activate the L2 example Pipeconf:
```
onos> app activate org.onosproject.p4tutorial.pipeconf
```

With the L2's pipeconf set, we are able to do packet I/O operations.

You should see a message response:
```
Activated org.onosproject.p4tutorial.pipeconf
```
The L2 pipeconf application is now activated in ONOS and awaits the switch connection to start performing P4Runtime operations.

On the terminal 3, we're iniciating the PvS Control Engine which listens to connections in the 50051 port. 
Instantiate the server:
```sh
$ ./run_p4runtime_server.sh
```

On terminal 4, we're informing ONOS of the devices that it needs to connect and let the interaction begin.
```sh
$ onos-netcfg localhost netconfig.json
```
This .json file has important information, like IP/port of the P4Runtime server, Device ID, ports, and other data.
```sh
{
  "devices": {
    "device:bmv2:l2": {
      "ports": {
        "1": {
        "name": "l2-eth1",
		"speed": 10000,
		"enabled": true,
		"number": 1,
		"removed": false,
		"type": "copper"
		}
	  },
	 "basic": {
		"managementAddress": "grpcs://127.0.0.1:50051?device_id=1",
		"driver": "bmv2"
	 }
	},
    "device:bmv2:router": {
      "ports": {
        "1": {
	"name": "router-eth1",
		"speed": 10000,
		"enabled": true,
		"number": 1,
		"removed": false,
		"type": "copper"
		}
	},
	"basic": {
	  "managementAddress": "grpcs://127.0.0.1:50051?device_id=2",
	  "driver": "bmv2"
	}
      }
    }
 }
```
The configuration is done. After, ONOS will be informed of the devices and initial P4Runtime requests can be made, containing Stream Channel Requests and Packet I/O.

How to perform other P4Runtime request operations between the controller and the control engine?

To perform packet-in operations, open terminal 5 and go to the root directory of the PvS Control Engine. Then, run the command to do a packet-in:
```sh
$ python example/packetin/packet_in_onos.py
```
You can see the packet-in being displayed in the ONOS log.

Now, in the ONOS CLI, we activate the L2 Switch App to perform a write request, and a packet-out.
The L2 Switch App creates a Flow Rule, and a Packet-Out operation that will appear in the control engine as the P4runtime Write request and Packet-Out request.
```
onos> app activate org.onosproject.p4tutorial.l2_switch
```
You should see a message response:
```
Activated org.onosproject.p4tutorial.l2_switch
```
The information of the write request, along with the Packet-out is shown in the control engine.


The integration is done. After, ONOS can show flow rules installed, applications instantiated, devices availability, and other operations.
If you wish to see the devices in the ONOS system, you can do it by two ways:
In the CLI, run the following command:
```
onos> devices
```
```
id=device:bmv2:l2, available=true, local-status=connected 19m45s ago, role=MASTER, type=SWITCH, mfr=p4.org, hw=master, sw=master, serial=unknown, chassis=0, driver=bmv2:org.onosproject.pipelines.basic, locType=none, managementAddress=grpcs://127.0.0.1:50051?device_id=1, name=device:bmv2:l2, p4DeviceId=1, protocol=P4Runtime
id=device:bmv2:router, available=true, local-status=connected 20h35m ago, role=MASTER, type=SWITCH, mfr=p4.org, hw=master, sw=master, serial=unknown, chassis=0, driver=bmv2:org.onosproject.pipelines.basic, locType=none, managementAddress=grpcs://127.0.0.1:50051?device_id=2, name=device:bmv2:router, p4DeviceId=2, protocol=P4Runtime
```
Also, there's a GUI in ONOS, where you can see the devices and other information.

To check other ONOS commands, use the command in the ONOS CLI:
```
onos> help onos
```

[developer section]: <https://wiki.onosproject.org/display/ONOS/Developer+Quick+Start>


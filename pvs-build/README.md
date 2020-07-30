# PvS Control Engine

This repository contains a functional P4Runtime server ready to use with virtual L2 and Router switches, with both builds available at the PvS Forwarding Engine repository.

To start the server, you need:
- [Ubuntu 16.04 or 18.04]
- [gRPC]
- [Protobuf]
- [PI]
- [Python 2.7]

To make this process easier, there's a script available in the [scripts] directory that installs everything. If one prefers a different method, feel free to follow the PI installation instructions.

## Installation Instructions

First, install Python and clone this repository:

```sh
$ sudo apt install python python-pip git
$ git clone https://github.com/pvs-conext/pvs-control-engine.git
$ cd pvs-control-engine
```

Then, make the script executable and run it:

```sh
$ chmod +x ./scripts/install_p4runtime.sh
$ ./scripts/install_p4runtime.sh
```

## Starting the P4Runtime Server

To run the PvS server, issue the following command:

```sh
$ chmod +x ./run_p4runtime_server.sh 
$ ./run_p4runtime_server.sh
```

## Running SDN Apps

There are toy examples of SDN apps in the [examples/sdn_apps] folder that you can use to create a stream channel with PvS Control Engine, authenticate the app, perform read/write table entries from/into virtual switches, process packet in/out from/to virtual switches, and read switch registers and counters. The "client_l2.py" file handles the L2 switch; "client_router.py" file handles the Router switch, and "client_int.py" handles the switch that does in-band telemetry.

In the main() methods, you may use any of the following methods to read, write, delete, or modify a switch table entry:

	1. WriteTableEntry()
	2. ReadTableEntry()
	3. DeleteTableEntry()

The WriteTableEntry() method may receive as update_type the following parameters:

	1. p4runtime_pb2.Update.INSERT - Insert a new entry in the switch table
	2. p4runtime_pb2.Update.MODIFY - Modifies an existing entry in the switch table

These apps are pre-configured to perform the set of actions as used in our evaluation, but you may modify their logic as you wish. After configuring the app to perform the desired actions, run the following commands:

```sh
$ export PYTHONPATH=.
$ python example_sdn_apps/client_[switch].py
```

Note that the server must be running before invoking a client. Also, make sure that the client is connecting to the correct TCP port, which must be the same as the server's.

The switches are deployed automatically into PvS using the LoadVSwitch.py script available in the [examples/virtual_switches] folder. The virtual switch codes are available in the [examples/virtual_switches/switch_code] folder. 

In case you experience issues during these steps, don't hesitate to check the [troubleshooting] file.

[//]: # "Links"

[Ubuntu 16.04 or 18.04]: <https://releases.ubuntu.com/>
[gRPC]: <https://grpc.io/docs/quickstart/python/>
[Protobuf]: <https://github.com/protocolbuffers/protobuf>
[PI]: <https://github.com/p4lang/PI>
[Python 2.7]: <https://www.python.org/>
[troubleshooting]: <https://github.com/pvs-conext/pvs-control-engine/blob/master/pvs-build/Troubleshooting.md>
[examples/virtual_switches]: <https://github.com/pvs-conext/pvs-control-engine/tree/master/pvs-build/examples/virtual_switches>
[examples/sdn_apps]: <https://github.com/pvs-conext/pvs-control-engine/tree/master/pvs-build/examples/sdn_apps>
[examples/virtual_switches/switch_code]: <https://github.com/pvs-conext/pvs-control-engine/tree/master/pvs-build/examples/virtual_switches/switch_code>


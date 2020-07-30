# Troubleshooting

## Issue 1
 I see something like the following when I try to start the PvS server:

```sh
$ python server/grpc_server.py
Loading l2 switch (id: 1), modules @ platform_api/lib/l2/, switch_data @ platform_api/lib/l2/switch_info.dat
Running load_switch_data for switch l2
Error adding switch l2. Fail
Running load_switch_modules for switch l2
Loading libcam for switch l2 (platform_api/lib/l2//libcam.so)
Traceback (most recent call last):
  File "server/grpc_server.py", line 73, in <module>
    LoadVSwitch.load_switches()
  File "/home/teste/p4runtime-grpc-v3/example_virtual_switches/LoadVSwitch.py", line 21, in load_switches
    PMA_mgmt.load_switch_modules("l2", "platform_api/lib/l2/", switch_id)
  File "/home/teste/p4runtime-grpc-v3/utils/PMA_mgmt.py", line 85, in load_switch_modules
    p4_tables_api.libcam_dict[switch_id]=cdll.LoadLibrary(dir_path + '/libcam.so')
  File "/usr/lib/python2.7/ctypes/__init__.py", line 444, in LoadLibrary
    return self._dlltype(name)
  File "/usr/lib/python2.7/ctypes/__init__.py", line 366, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: libsumereg.so: cannot open shared object file: No such file or directory
```

**How to solve it:** your LD_LIBRARY_PATH environment variable is not set. You can export it as shown in the main [README], or run this script located inside the PvS Data Plane project:

```sh
$ source /scripts/settings.sh
```

## Issue 2
Whenever I try to run the server or client, there's this import error:

```sh
Traceback (most recent call last):
  File "grpc_server.py", line 11, in <module>
    from protobuffs import p4runtime_pb2 as p4runtime_pb2
ImportError: No module named protobuffs
```

**How to solve it:** you might be running the server/client from inside a directory that's not the root (e.g. p4runtime-grpc-v3/server/). Go back to the project's root folder and try to run the server/client from there. Make sure that you followed the "export" instructions mentioned in the [README] correctly.

## Issue 3
When I run the client, the system returns the following error: 

```sh
status = StatusCode.UNAVAILABLE
	details = "failed to connect to all addresses"
	debug_error_string = "{"created":"@1589319595.460314133","description":"Failed to pick subchannel","file":"src/core/ext/filters/client_channel/client_channel.cc","file_line":3981,"referenced_errors":[{"created":"@1589319595.460309728","description":"failed to connect to all addresses","file":"src/core/ext/filters/client_channel/lb_policy/pick_first/pick_first.cc","file_line":394,"grpc_status":14}]}"
```

**How to solve it:** the server might not be running. Check if the 50051 port is being used in the system with the following command, and if it is, kill the process that's using it:

```sh
$ netstat -lpnt | grep "50051"
$ kill -SIGKILL <pid>
```

If the process is a Python script, it'll appear as "\<pid>/python", for example.

## Issue 4
The server is already running, but when I run the client, the server returns the following message:

```sh
CAM_Init_ValidateContext() - done
python: ioctl: No such device
```
**How to solve it:** the server and client both worked successfully. However, there's not a NetFPGA connection available.

[//]: # "Links"

[README]: <https://github.com/pvs-conext/pvs-control-engine/blob/master/README.md>

#!/usr/bin/python3
#
# This command receives statistics from Ganesha over DBus. The format
# for a command is:
#
# ganesha_stats <subcommand> <args>
#
# ganesha_stats help
#       To get detaled help
#
from __future__ import print_function
import sys
import Ganesha.glib_dbus_stats

def usage():
    message = "Command displays global stats by default.\n"
    message += "To display current status regarding stat counting use \n"
    message += "%s status \n" % (sys.argv[0])
    message += "To display stat counters use \n"
    message += "%s [list_clients | deleg <ip address> | " % (sys.argv[0])
    message += " inode | iov3 [export id] | iov4 [export id] | export |"
    message += " total [export id] | fast | pnfs [export id] |"
    message += " fsal <fsal name> | v3_full | v4_full | auth |"
    message += " client_details <ip address> | export_details <export id>] \n"
    message += "To reset stat counters use \n"
    message += "%s reset \n" % (sys.argv[0])
    message += "To enable/disable stat counters use \n"
    message += "%s [enable | disable] [all | nfs | fsal | v3_full | " % (sys.argv[0])
    message += "v4_full | auth] \n"
    sys.exit(message)

if (len(sys.argv) < 2):
    command = 'global'
else:
    command = sys.argv[1]

# check arguments
commands = ('help', 'list_clients', 'deleg', 'global', 'inode', 'iov3', 'iov4',
            'export', 'total', 'fast', 'pnfs', 'fsal', 'reset', 'enable',
            'disable', 'status', 'v3_full', 'v4_full', 'auth', 'client_details',
            'export_details')
if command not in commands:
    print("Option '%s' is not correct." % command)
    usage()
# requires an IP address
elif command in ('deleg', 'client_details'):
    if not len(sys.argv) == 3:
        print("Option '%s' must be followed by an ip address." % command)
        usage()
    command_arg = sys.argv[2]
# requires an export id
elif command == 'export_details':
    if not len(sys.argv) == 3:
        print("Option '%s' must be followed by an export id." % command)
        usage()
    if sys.argv[2].isdigit():
        command_arg = int(sys.argv[2])
    else:
        print("Argument '%s' must be numeric." % sys.argv[2])
        usage()
# optionally accepts an export id
elif command in ('iov3', 'iov4', 'total', 'pnfs'):
    if (len(sys.argv) == 2):
        command_arg = -1
    elif (len(sys.argv) == 3) and sys.argv[2].isdigit():
        command_arg = int(sys.argv[2])
    else:
        usage()
# requires fsal name
elif command in ('fsal'):
    if not len(sys.argv) == 3:
        print("Option '%s' must be followed by fsal name." % command)
        usage()
    command_arg = sys.argv[2]
elif command in ('enable', 'disable'):
    if not len(sys.argv) == 3:
        print("Option '%s' must be followed by all/nfs/fsal/v3_full/v4_full/auth" %
              command)
        usage()
    command_arg = sys.argv[2]
    if command_arg not in ('all', 'nfs', 'fsal', 'v3_full', 'v4_full', 'auth'):
        print("Option '%s' must be followed by all/nfs/fsal/v3_full/v4_full/auth" %
              command)
        usage()
elif command == "help":
    usage()

# retrieve and print stats
exp_interface = Ganesha.glib_dbus_stats.RetrieveExportStats()
cl_interface = Ganesha.glib_dbus_stats.RetrieveClientStats()
if command == "global":
    print(exp_interface.global_stats())
elif command == "export":
    print(exp_interface.export_stats())
elif command == "inode":
    print(exp_interface.inode_stats())
elif command == "fast":
    print(exp_interface.fast_stats())
elif command == "list_clients":
    print(cl_interface.list_clients())
elif command == "deleg":
    print(cl_interface.deleg_stats(command_arg))
elif command == "client_details":
    print(cl_interface.client_details_stats(command_arg))
elif command == "iov3":
    print(exp_interface.v3io_stats(command_arg))
elif command == "iov4":
    print(exp_interface.v4io_stats(command_arg))
elif command == "total":
    print(exp_interface.total_stats(command_arg))
elif command == "export_details":
    print(exp_interface.export_details_stats(command_arg))
elif command == "pnfs":
    print(exp_interface.pnfs_stats(command_arg))
elif command == "reset":
    print(exp_interface.reset_stats())
elif command == "fsal":
    print(exp_interface.fsal_stats(command_arg))
elif command == "v3_full":
    print(exp_interface.v3_full_stats())
elif command == "v4_full":
    print(exp_interface.v4_full_stats())
elif command == "auth":
    print(exp_interface.auth_stats())
elif command == "enable":
    print(exp_interface.enable_stats(command_arg))
elif command == "disable":
    print(exp_interface.disable_stats(command_arg))
elif command == "status":
    print(exp_interface.status_stats())

#!/usr/bin/env python3
# Script to run android build commands in a more convenient way
# Note: replace `package` and `launch_activity` with your own
# Author: Amanda M. Watson (amwatson)

import sys
from subprocess import call

# ================
# Global constants
# ================

package = "com.someorg.packagename"
launch_activity = ".MainActivity"

# ========================
# Global mutable variables
# ========================

has_executed_build = False

# ================
# Helper functions
# ================

def shell_cmd(cmd):
    return call(cmd.split())

def adb_shell_cmd(cmd):
    return shell_cmd("adb shell " + cmd)

# ==================
# Available commands
# ==================

def start(_):
    return adb_shell_cmd("am start %s/%s" % (package, launch_activity))

def stop(_):
    return adb_shell_cmd("am force-stop %s" % package)

def install(build_config):
    return shell_cmd("./gradlew install%s" % build_config)

def uninstall(build_config):
    return shell_cmd("./gradlew uninstall%s" % build_config)

def build(build_config):
    return shell_cmd("./gradlew assemble%s" % build_config)

def clean(_):
    return shell_cmd("./gradlew clean")

# Main

def main():
    argv = sys.argv[1:]
    if len(argv) == 0:
        print(
    """Usage: build.py [debug | profile | release] <options...>
    options:
        - build
        - install
        - uninstall
        - start
        - stop
        - clean
    Options will execute in order, e.g. cmd.py clean build install start stop uninstall""")
        exit(-1)

    build_configs = ["debug", "profile", "release"]
    active_build_config = "profile"
    if (argv[0] in build_configs):
        active_build_config = argv[0]
        argv = argv[1:]

    for idx, arg in enumerate(argv):
        try:
            if (globals()[arg](active_build_config.capitalize()) != 0):
                if (arg == "install" and active_build_config == "release"):
                    print("**Warning: this command fails if a release keystore is not specified")
                if (len(argv[idx+1:]) > 0):
                    print("ERROR: The following commands were not executed: ", argv[idx+1:])
                    exit(-2)
                elif (arg == "build"):
                        has_executed_build = True
        except KeyError:
            print("Error: unrecognized command '%s'" % arg)
            exit(-3)

if __name__ == "__main__":
    main()

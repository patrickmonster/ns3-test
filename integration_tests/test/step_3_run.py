# The MIT License (MIT)
#
# Copyright (c) 2020 ETH Zurich
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import exputil
import time

try:
    from .run_list import *
except (ImportError, SystemError):
    from run_list import *

local_shell = exputil.LocalShell()
max_num_processes = 4

# Check that no screen is running
if local_shell.count_screens() != 0:
    print("There is a screen already running. "
          "Please kill all screens before running this analysis script (killall screen).")
    exit(1)

# Generate the commands
# commands_to_run = []
for run in get_tcp_run_list():
    
    commands_to_run.append(
        "cd ../ns-allinone-3.37/ns-3.37;"
        "./ns3 run broadcast"
    )


# # Run the commands
# print("Running commands (at most %d in parallel)..." % max_num_processes)
# for i in range(len(commands_to_run)):
#     print("Starting command %d out of %d: %s" % (i + 1, len(commands_to_run), commands_to_run[i]))
#     local_shell.detached_exec(commands_to_run[i])
#     while local_shell.count_screens() >= max_num_processes:
#         time.sleep(2)


# print("Starting command %d out of %d: %s" % (i + 1, len(commands_to_run), commands_to_run[i]))
local_shell.detached_exec("cd ../../ns-allinone-3.37/ns-3.37; ./ns3 run broadcast.py")
while local_shell.count_screens() >= max_num_processes:
    time.sleep(2)


# Awaiting final completion before exiting
print("Waiting completion of the last %d..." % max_num_processes)
while local_shell.count_screens() > 0:
    time.sleep(2)
print("Finished.")

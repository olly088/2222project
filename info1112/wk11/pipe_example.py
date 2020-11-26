# Adapted from Gios example

import os
import sys

name = sys.argv[1]

# Program you will be using to execute the code when you exec
cmd = '/bin/python3'

# Generate file descriptors for pipe
read_end, write_end = os.pipe()

pid = os.fork()
if pid > 0:
    # Parent process
    ret_val = os.wait() # Wait for child to finish, rturns its exit status, see os.wait() docs for format
    bytes_from_pipe = os.read(read_end, 100) # Read 100 bytes of pipe contents 

    print(bytes_from_pipe.decode().strip())

    os.close(read_end)
    os.close(write_end)

elif pid == 0:
    # Child process)
    os.dup2(write_end, 1) # Replace its STDOUT fd with the one retunred from the pipe
    os.execv(cmd, (cmd, "mn.py")) # Execute the program, will output to the pipe

else:
    print("FORK ERROR")
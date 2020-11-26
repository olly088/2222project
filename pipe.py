import os
import sys

pipein, pipeout = os.pipe()
if os.fork():
    # parent
    os.wait()
    
    os.close(pipeout)

    pol = os.fdopen(pipeout)
    data = pol.readlines()
    print(data)

    #os.close(pipeout)
    os.dup2(pipein, 0)
    #os.execl("/bin/python3", "/bin/python3", "abc.py")
    os._exit(127)

else:
    # child
    os.close(pipein)
    os.dup2(pipeout, 1)
    os.execl("/bin/python3", "/bin/python3", "abc.py")

    os._exit(127)


pid = os.fork()
#os.dup2(1, w)







#if pid == 0:
    #os.dup2(1, w)
    #print("Writing to pipe")
    #os.execl("/bin/python3", "/bin/python3", "abc.py")
    #os.close(r)
    #writing_end = os.fdopen(w, 'w')
    #os.execl("/bin/python3", "/bin/python3", "abc.py")
    #writing_end.write("hello")
    #sys.exit(1)

#else:
    #os.wait()
    #os.close(w)
    #reading_end = os.fdopen(r)
    #output = reading_end.read()
    #print(output)

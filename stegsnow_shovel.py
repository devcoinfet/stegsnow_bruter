#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import os
import sys
import subprocess
import codecs
from threading import Thread, Lock
from multiprocessing import Process, cpu_count

THREADS = 4

PROCESS =  cpu_count() * 2
lock = Lock() 
attempted_cracks = []
nrockyoulist = []

'''
f = open(sys.argv[1],encoding="latin-1")

rockyoulist = f.readlines() 
for item in rockyoulist:
    nrockyoulist.append(item.strip())

'''
def get_passes(dataset_path):
    
    ips = []

    file = open(dataset_path, "r")
    dataset = list(filter(None, file.read().split("\n")))
    
    for line in dataset:
        ips.append(line.rstrip())
        print(line)

    return ips

def passwords_process(a, n):
    #ode to devil the best coder i know ;)
    k, m = divmod(len(a), n)
    for i in range(n):
        yield a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]


def stegsnow_crack(pass_in):
    print("Attempting to crack flaggy.txt with :"+str(len(pass_in))+" Passwords For this thread")  
    
    for item in pass_in:
        try:
           cmd = ('stegsnow -C -p {} flaggy.txt').format(item.rstrip())
           print(cmd)
           sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
           output = ""
           while True:
               out = sp.stdout.read(1).decode('utf-8')
               if out == '' and sp.poll() != None:
                  break
               if out != '':
                  output += out
                  sys.stdout.write(out)
                  sys.stdout.flush()
        
           if output:
              for item in output.split():
                  attempted_cracks.append(item)
            
              return output.split()

        except Exception as ohshits:
             print(ohshits)
             pass

    
if __name__ == "__main__":
   #use iterator and chop rockyou into smaller pieces
   password_list  = get_passes(sys.argv[1])
   passwords = passwords_process(password_list,PROCESS)
   for _ in range(PROCESS):
       p = Thread(target=stegsnow_crack, args=(next(passwords), ))
       p.daemon = True
       p.start()

   for _ in range(PROCESS):
       p.join()
       
for found in attempted_cracks:
    if "csictf{" in found:
        print("FLAG FOUND :"+str(found))
        sys.exit()
    else:
        print("No flaggy for youz :"+str(found))
        pass

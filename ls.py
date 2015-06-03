from subprocess import Popen, PIPE
from time import sleep
import sys
import re

def ls(directory):
    p1 = Popen(['ls', '-lR', directory], stdout=PIPE)

    p2 = Popen(['grep', '^-'], stdin=p1.stdout, stdout=PIPE)

    p3 = Popen(["awk", r'{print $9}'], stdin=p2.stdout, stdout=PIPE)

    files, err = p3.communicate()

    return files.strip().split()


def scan_new_files(directory):
    
    while True:
        files = ls(directory)
        if files:
            print(files)    

        sleep(30)
    
DIR = sys.argv[1]

scan_new_files(DIR)

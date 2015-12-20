import time
import os
import subprocess, threading
from subprocess import PIPE
import signal
import psutil


class Command(object):
    def __init__(self, cmd, output=PIPE, shell=False):
        self.cmd = cmd
        self.output = output
        self.shell = shell
        self.process = None

    def run(self, timeout):
        status = "OK"
        def target():
            print 'Thread started'
            self.process.communicate()
            print "PROCESS STATUS CODE " + str(self.process.returncode)
            print 'Thread finished'

        self.process = psutil.Popen(self.cmd, stdout=self.output, stderr=self.output, shell=self.shell)
        parent_pid = self.process.pid
        thread = threading.Thread(target=target)
        thread.start()

        time.sleep(1) # short delay to give time for vaa3d to launch
        child_processes = self.get_child_processes(parent_pid)
        print "Children = " + str(child_processes)
        
        thread.join(timeout)
        if thread.is_alive():
            status = "TIMEOUT"
            print 'Terminating process'
            try:
                self.process.terminate()
            except:
                print "Thread active but process already completed?"
            thread.join()
        self.cleanup(child_processes)
        return status

    def get_child_processes(self, parent_pid):
        try:
            p = psutil.Process(parent_pid)
        except psutil.NoSuchProcess:
            return []
        return p.get_children(recursive=True)

    def cleanup(self, processes):
        for process in processes:
            try:
                process.send_signal(signal.SIGTERM)
            except:
                print "PID cannot be killed because it does not exist"


import os
import sys
import syslog
import time
from Gauge import *
from OBD import *
from Pipeline import *
from threading import Thread, Lock

OUTGOING_FIFO_NAME="gauge2gui"
INCOMING_FIFO_NAME="gui2gauge"

if __name__ == "__main__":
    # Connect to OBD2 device
    obdConnection = OBDConnector()
    while not obdConnection.connect():
        syslog.syslog(syslog.LOG_ERR, 'Main: OBD Connector failed to connect')
        time.sleep(1)
    
    while not obdConnection.isConnected():
        syslog.syslog(syslog.LOG_ERR, 'Main: OBD Connector not established for car. Retring')
        time.sleep(1)
    
    # Initialise the queues system
    responsesQueue = ResponseQ()
    responsesQueue.start()
    obdDispatcher = CommandDispatcher(obdConnection, responsesQueue)
    obdDispatcher.start()
    jobManager = TimedJobManager()

    #Set up IPC
    jobs = dict

    out_fs = None
    in_fs = None

    try:
        os.mkfifo(OUTGOING_FIFO_NAME)
        os.mkfifo(INCOMING_FIFO_NAME)
        try:
            out_fs = os.open(OUTGOING_FIFO_NAME, os.O_WRONLY | os.O_APPEND | os.O_CREAT)
            in_fs = os.open(INCOMING_FIFO_NAME, os.O_RDONLY, os.O_CREAT)

            GaugeModule = __import__("Gauge")

            for packet in in_fs:
                cmd, freq = packet.split(':')
                action = cmd[0]
                cmd = cmd[1, -1]

                gaugeClassName = "Gauge" + cmd
                gaugeClass = getattr(GaugeModule, gaugeClassName)
                gaugeObj = gaugeClass(freq, out_fs) # construct a gauge object
                gaugeJob = gaugeObj.toJob() #convert it to a job object
                if action == "+":
                    jobManager.watch(gaugeObj.frequency, gaugeJob, obdDispatcher)  

                elif action == "-":
                    jobManager.unwatch(freq, gaugeObj.obdCommand)

        finally:
            if out_fs is not None:
                os.close(out_fs)
            if in_fs is not None:
                os.close(in_fs)

    finally:
        os.remove(OUTGOING_FIFO_NAME)
        os.remove(INCOMING_FIFO_NAME)
    

threading.join()

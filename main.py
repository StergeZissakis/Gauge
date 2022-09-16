import os
import sys
import syslog
import time
import socket
from Gauge import *
from OBD import *
from Pipeline import *
from threading import Thread, Lock

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 5656))
    outSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    GaugeModule = __import__("Gauge")

    while True:
        packet = ""
        char = sock.recv(1)
        while char != '\n':
            packet += str(char)
            char = sock.recv(1)
            print(char)
        
        print(packet)
        cmd, freq = packet.split(':')
        action = cmd[0]
        cmd = cmd[1:-1]

        gaugeClassName = "Gauge" + cmd
        gaugeClass = getattr(GaugeModule, gaugeClassName)
        gaugeObj = gaugeClass(freq, outSock) # construct a gauge object
        gaugeJob = gaugeObj.toJob() #convert it to a job object
        if action == "+":
            jobManager.watch(gaugeObj.frequency, gaugeJob, obdDispatcher)  
        elif action == "-":
            jobManager.unwatch(freq, gaugeObj.obdCommand)



import os
import sys
import syslog
import time
import socket
from Gauge import *
from OBD import *
from Pipeline import *
from threading import Thread, Lock

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


rpmGauge = GaugeRPM()
klmGauge = GaugeKLM()

row = pn.Row(klmGauge.gaugeUI, rpmGauge.gaugeUI)
gaugeBox = pn.WidgetBox(row)
gaugeBox.servable()


jobManager.watch(rpmGauge.frequency, rpmGauge.toJob(), obdDispatcher)
jobManager.watch(klmGauge.frequency, klmGauge.toJob(), obdDispatcher)

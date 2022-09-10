import syslog
import time
from OBD import *
from Gauge import *
import time
import panel as pn
from Pipeline import *
pn.extension('echarts')

obdConnection = OBDConnector()
while not obdConnection.connect():
    syslog.syslog(syslog.LOG_ERR, 'Main: OBD Connector failed to connect')
    time.sleep(1)

rpmGauge = GaugeRPM()
klmGauge = GaugeSpeed()

row = pn.Row(klmGauge.gaugeUI, rpmGauge.gaugeUI)
gaugeBox = pn.WidgetBox(row)
gaugeBox.servable()

while not obdConnection.isConnected():
    syslog.syslog(syslog.LOG_ERR, 'Main: OBD Connector not established for car. Retring')
    time.sleep(1)

responsesQueue = ResponseQ()
responsesQueue.start()

obdDispatcher = CommandDispatcher(obdConnection, responsesQueue)
obdDispatcher.start()

jobManager = TimedJobManager()

rpmJob = GaugeToJob(rpmGauge)
jobManager.watch(rpmGauge.frequency, rpmJob, obdDispatcher)  
klmJob = GaugeToJob(klmGauge)
jobManager.watch(klmGauge.frequency, klmJob, obdDispatcher)  

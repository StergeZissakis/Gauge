import sys
import syslog
import time
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from Gauge import *
from OBD import *
from Pipeline import *
import signal
from dash import Dash, html, dcc, Input, Output
import dash_daq as daq

signal.signal(signal.SIGINT, signal.SIG_DFL)

app = Dash(__name__)

obdConnection = OBDConnector()
while not obdConnection.connect():
	syslog.syslog(syslog.LOG_ERR, 'Main: OBD Connector failed to connect')
	time.sleep(1)

rpmGauge = GaugeRPM()
klmGauge = GaugeSpeed()

app.layout = html.Div(children=[html.Div([rpmGauge.gaugeUI]),html.Div([klmGauge.gaugeUI])])


while not obdConnection.isConnected():
	syslog.syslog(syslog.LOG_ERR, 'Main: OBD Connector not established for car. Retring')
	time.sleep(1)

responsesQueue = ResponseQ()
responsesQueue.start()

obdDispatcher = CommandDispatcher(obdConnection, responsesQueue)
obdDispatcher.start()

jobManager = TimedJobManager()

rpmJob = rpmGauge.toJob()
jobManager.watch(rpmGauge.frequency, rpmJob, obdDispatcher)  
klmJob = klmGauge.toJob()
jobManager.watch(klmGauge.frequency, klmJob, obdDispatcher)  


if __name__ == "__main__":
    app.run_server(debug=True)

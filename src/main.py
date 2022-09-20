import sys
import syslog
import time
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from Gauge import *
from OBD import *
from Pipeline import *
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":
	app = QApplication(sys.argv)

	w = QWidget()
	w.resize(1024,768)
	w.setWindowTitle("Gauge")

	obdConnection = OBDConnector()
	while not obdConnection.connect():
		syslog.syslog(syslog.LOG_ERR, 'Main: OBD Connector failed to connect')
		time.sleep(1)
	
	rpmGauge = GaugeRPM()
	klmGauge = GaugeSpeed()
	intakePressureGauge = GaugeIntakePressure()
	intakeTempGauge = GaugeIntakeTemp()
	oilTempGauge = GaugeOilTemp()
	coolantTempGauge = GaugeCoolantTemp()
	
	grid = QGridLayout(w)

	grid.addWidget(rpmGauge.gaugeUI, 0, 0)
	grid.addWidget(klmGauge.gaugeUI, 0, 1)
	grid.addWidget(oilTempGauge.gaugeUI, 0, 2)
	grid.addWidget(intakePressureGauge.gaugeUI, 1, 0)
	grid.addWidget(intakeTempGauge.gaugeUI, 1, 1)
	grid.addWidget(coolantTempGauge.gaugeUI, 1, 2)
	
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

	oilTempJob = oilTempGauge.toJob()
	jobManager.watch(oilTempGauge.frequency, oilTempJob, obdDispatcher)  

	intakePressureJob = intakePressureGauge.toJob()
	jobManager.watch(intakePressureGauge.frequency, intakePressureJob, obdDispatcher)  

	intakeTempJob = intakeTempGauge.toJob()
	jobManager.watch(intakeTempGauge.frequency, intakeTempJob, obdDispatcher)  

	coolantTempJob = coolantTempGauge.toJob()
	jobManager.watch(coolantTempGauge.frequency, coolantTempJob, obdDispatcher)  

	w.show()
	sys.exit(app.exec_())

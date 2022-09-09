from OBDAsync import *
from Meters import *
import time
import panel as pn

pn.extension('echarts')

asyncConnection = OBDAsyncConnector()
asyncConnection.connect()
monitor = OBDAsyncMonitor(asyncConnection)

rpmGauge = pn.indicators.Gauge(name='RPM', value=0, bounds=(0, 6000))
klmGauge = pn.indicators.Gauge(name='klmh', value=0, bounds=(0, 220))

rpmMeter = Meter_RPM(monitor, rpmGauge)
speedMeter = Meter_Speed(monitor, klmGauge)

row = pn.Row(klmGauge, rpmGauge)
gaugeBox = pn.WidgetBox(row)
gaugeBox.servable()

if asyncConnection.isConnected():
    rpmMeter.startReadings()
    speedMeter.startReadings()

    monitor.start()
    #time.sleep(60)
    #monitor.stop()
    #monitor.finish()
    #asyncConnection.disconnect()


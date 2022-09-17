import obd
from Pipeline import Job
from  analoggaugewidget import *
from dash import Dash, html, dcc, Input, Output
import dash_daq as daq

class Gauge:
    obdCommand = None
    gaugeUI = None
    frequency = None

    def __init__(self, command, freq):
        self.obdCommand = command
        self.frequency = freq

    def getValue(self, value):
        return int(value)

    def processReading(self, reading):
        val = self.getValue(reading.value.magnitude)

    def toJob(self):
        return Job(self)

class GaugeRPM(Gauge):

    def __init__(self):
        super(GaugeRPM, self).__init__(obd.commands.RPM, 100)
        self.gaugeUI = daq.Gauge(
                id='gauge-rpm-id',
                label='rpm',
                value=0,
                min=0,
                max=9000,
                units='rpm',
                #color="#9B51E0",
                color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
                scale={'start': 0, 'interval': 1000, 'labelInterval': 7000},
                size=300, #the side of the gague in pixels
                )


class GaugeSpeed(Gauge):

    def __init__(self):
        super(GaugeSpeed, self).__init__(obd.commands.SPEED, 100)
        self.gaugeUI = daq.Gauge(
                id='gauge-klm-id',
                label='klm/h',
                value=0,
                min=0,
                max=260,
                units='klm/h',
                #color="#9B51E0",
                color={"gradient":True,"ranges":{"green":[0,6],"yellow":[6,8],"red":[8,10]}},
                scale={'start': 0, 'interval': 10, 'labelInterval': 220},
                size=300, #the side of the gague in pixels
                )


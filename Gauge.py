import obd
from Pipeline import Job
from  analoggaugewidget import *

class Gauge:
    obdCommand = None
    gaugeUI = None
    frequency = None

    def __init__(self, command, freq):
        self.obdCommand = command
        self.frequency = freq

    def processReading(self, reading):
        val = reading.value.magnitude
        #self.gaugeUI.value = val
        self.gaugeUI.update_value(val)

    def toJob(self):
        return Job(self)

class GaugeRPM(Gauge):

    def __init__(self):
        super(GaugeRPM, self).__init__(obd.commands.RPM, 100)
        self.gaugeUI = AnalogGaugeWidget()
        self.gaugeUI.set_MaxValue(6000)
        self.gaugeUI.set_enable_ScaleText(True)
        self.gaugeUI.set_enable_value_text(True)
        self.gaugeUI.setMouseTracking(False)


class GaugeSpeed(Gauge):

    def __init__(self):
        super(GaugeSpeed, self).__init__(obd.commands.SPEED, 100)
        self.gaugeUI = AnalogGaugeWidget()
        self.gaugeUI.set_MaxValue(280)
        self.gaugeUI.set_enable_ScaleText(True)
        self.gaugeUI.set_enable_value_text(True)
        self.gaugeUI.setMouseTracking(False)

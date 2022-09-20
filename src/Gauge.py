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

    def getValue(self, reading):
        return int(reading.value.magnitude)

    def processReading(self, reading):
        val = self.getValue(reading)
        self.gaugeUI.update_value(val)

    def toJob(self):
        return Job(self)

    def applyGaugeCommonAttributes(self):
        self.gaugeUI.set_enable_ScaleText(True)
        self.gaugeUI.set_enable_value_text(True)
        self.gaugeUI.setMouseTracking(False)

class GaugeRPM(Gauge):

    def __init__(self):
        super(GaugeRPM, self).__init__(obd.commands.RPM, 100)
        self.gaugeUI = AnalogGaugeWidget()
        self.gaugeUI.set_MinValue(0)
        self.gaugeUI.set_MaxValue(9000)
        self.applyGaugeCommonAttributes()


class GaugeSpeed(Gauge):

    def __init__(self):
        super(GaugeSpeed, self).__init__(obd.commands.SPEED, 100)
        self.gaugeUI = AnalogGaugeWidget()
        self.gaugeUI.set_MinValue(0)
        self.gaugeUI.set_MaxValue(280)
        self.applyGaugeCommonAttributes()

class GaugeOilTemp(Gauge):

    def __init__(self):
        super(GaugeOilTemp, self).__init__(obd.commands.OIL_TEMP, 500)
        self.gaugeUI = AnalogGaugeWidget()
        self.gaugeUI.set_MinValue(0)
        self.gaugeUI.set_MaxValue(140)
        self.applyGaugeCommonAttributes()

class GaugeCoolantTemp(Gauge):

    def __init__(self):
        super(GaugeCoolantTemp, self).__init__(obd.commands.COOLANT_TEMP, 500)
        self.gaugeUI = AnalogGaugeWidget()
        self.gaugeUI.set_MinValue(0)
        self.gaugeUI.set_MaxValue(140)
        self.applyGaugeCommonAttributes()

class GaugeIntakePressure(Gauge):

    def __init__(self):
        super(GaugeIntakePressure, self).__init__(obd.commands.INTAKE_PRESSURE, 300)
        self.gaugeUI = AnalogGaugeWidget()
        self.gaugeUI.set_MaxValue(0)
        self.gaugeUI.set_MaxValue(300)
        self.applyGaugeCommonAttributes()

class GaugeIntakeTemp(Gauge):

    def __init__(self):
        super(GaugeIntakeTemp, self).__init__(obd.commands.INTAKE_TEMP, 300)
        self.gaugeUI = AnalogGaugeWidget()
        self.gaugeUI.set_MaxValue(0)
        self.gaugeUI.set_MaxValue(140)
        self.applyGaugeCommonAttributes()



class SolidGauge(Gauge):

    def __init__(self, command, freq):
        super(SolidGauge, self).__init__(command, freq)

    def processReading(self, reading):
        val = self.getValue(reading)
        self.gaugeUI.value = val

    def applyGaugeCommonAttributes(self):
        pass



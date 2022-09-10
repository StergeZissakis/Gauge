import obd
from Pipeline import Job
import panel as pn
pn.extension('echarts')

class Gauge:
    obdCommand = None
    gaugeUI = None
    frequency = None

    def __init__(self, command, freq):
        self.obdCommand = command
        self.frequency = freq

    def processReading(self, reading):
        val = reading.value.magnitude
        self.gaugeUI.value = val

def GaugeToJob(gauge):
    ret = Job()
    ret.gauge = gauge
    return ret


class GaugeRPM(Gauge):

    def __init__(self):
        super(GaugeRPM, self).__init__(obd.commands.RPM, 100)
        self.gaugeUI = pn.indicators.Gauge(name='RPM', value=0, bounds=(0, 9000))


class GaugeSpeed(Gauge):

    def __init__(self):
        super(GaugeSpeed, self).__init__(obd.commands.SPEED, 200)
        self.gaugeUI = pn.indicators.Gauge(name='klmh', value=0, bounds=(0, 220))


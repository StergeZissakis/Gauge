import obd
from Pipeline import Job
import panel as pn
pn.extension('echarts')

class Gauge:
    obdCommand = None
    gaugeUI = None
    frequency = None
    tag = None

    def __init__(self, command, freq, tag):
        self.obdCommand = command
        self.frequency = freq
        self.teg = tag

    def getValue(self, reading):
        return int(reading.value.magnitude)

    def processReading(self, reading):
        self.gaugeUI.value = self.getValue(reading)

    def toJob(self):
        return Job(self)

class GaugeRPM(Gauge):

    def __init__(self):
        super(GaugeRPM, self).__init__(obd.commands.RPM, 100, "RPM")
        self.gaugeUI = pn.indicators.Gauge(name='RPM', value=0, bounds=(0, 9000))


class GaugeKLM(Gauge):

    def __init__(self):
        super(GaugeKLM, self).__init__(obd.commands.SPEED, 200, "KLM")
        self.gaugeUI = pn.indicators.Gauge(name='klmh', value=0, bounds=(0, 220))

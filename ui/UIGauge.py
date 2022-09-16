import obd
import panel as pn
pn.extension('echarts')

class UIGauge:
    name = None
    gaugeUI = None
    frequency = None

    def __init__(self, name, freq):
        self.name = name
        self.frequency = freq

    def setValue(self, value):
        self.gaugeUI.value = value

    def toPacket(self):
        return self.name + ":" + str(self.frequency) + "\n"


class GaugeRPM(UIGauge):

    def __init__(self):
        super(GaugeRPM, self).__init__("RPM", 100)
        self.gaugeUI = pn.indicators.Gauge(name='RPM', value=0, bounds=(0, 9000))


class GaugeKLM(UIGauge):

    def __init__(self):
        super(GaugeKLM, self).__init__("KLM", 200)
        self.gaugeUI = pn.indicators.Gauge(name='klmh', value=0, bounds=(0, 220))


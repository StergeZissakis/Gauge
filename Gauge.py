import obd
from Pipeline import Job

class Gauge:
    obdCommand = None
    gaugeUI = None
    frequency = None
    tag = None
    ipcPipe = None

    def __init__(self, command, freq, tag, pipe):
        self.obdCommand = command
        self.frequency = freq
        self.teg = tag
        self.ipcPipe = pipe

    def getValue(self, reading):
        return int(reading.value.magnitude)

    def processReading(self, reading):
        packet = tag + ":" + self.getValue(reading) + '\n'
        self,ipcPipe.write(packet)


    def toJob(self):
        return Job(self)

class GaugeRPM(Gauge):

    def __init__(self, freq, pipe):
        super(GaugeRPM, self).__init__(obd.commands.RPM, freq, "RPM", pipe)


class GaugeKLM(Gauge):

    def __init__(self, freq, pipe):
        super(GaugeKLM, self).__init__(obd.commands.SPEED, freq, "KLM", pipe)

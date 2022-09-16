import obd
from Pipeline import Job

class Gauge:
    obdCommand = None
    gaugeUI = None
    frequency = None
    tag = None
    sock = None

    def __init__(self, command, freq, tag, sock):
        self.obdCommand = command
        self.frequency = freq
        self.teg = tag
        self.sock = sock

    def getValue(self, reading):
        return int(reading.value.magnitude)

    def processReading(self, reading):
        packet = tag + ":" + self.getValue(reading) + '\n'
        self.sock.sendto(packet, "127.0.0.1", 5657)

    def toJob(self):
        return Job(self)

class GaugeRPM(Gauge):

    def __init__(self, freq, sock):
        super(GaugeRPM, self).__init__(obd.commands.RPM, freq, "RPM", sock)


class GaugeKLM(Gauge):

    def __init__(self, freq, sock):
        super(GaugeKLM, self).__init__(obd.commands.SPEED, freq, "KLM", sock)

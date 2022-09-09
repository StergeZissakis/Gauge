import obd
import syslog

class Meter:
    obdCommand = None
    obdMonitor = None
    gauge = None

    def __init__(self, command, monitor, gauge):
        self.obdCommand = command
        self.obdMonitor = monitor
        self.gauge = gauge

    def processReading(self, reading):
        pass

    def tick(self, reading):
        if reading:
            self.processReading(reading)

    def startReadings(self):
        self.obdMonitor.startMonitoring(self.obdCommand, self.tick)

    def stopReadings(self):
        self.obdMonitor.stopMonitoring(self.obdCommand)



class Meter_RPM(Meter):
    obdCommand = obd.commands.RPM

    def __init__(self, monitor, gauge):
        super(Meter_RPM, self).__init__(self.obdCommand, monitor, gauge)


    def processReading(self, reading):
        val = reading.value.magnitude
        self.gauge.value = val


class Meter_Speed(Meter):
    obdCommand = obd.commands.SPEED

    def __init__(self, monitor, gauge):
        Meter.__init__(self, self.obdCommand, monitor, gauge)


    def processReading(self, reading):
        val = reading.value.magnitude
        self.gauge.value = val

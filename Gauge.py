import obd
import syslog

class Gauge:
    obdCommand = None
    obdMonitor = None

    def __init__(self, command, monitor):
        self.obdCommand = command
        self.obdMonitor = monitor

    def processReading(self, reading):
        pass

    def tick(self, reading):
        if reading:
            self.processReading(reading)

    def startReadings(self):
        self.obdMonitor.startMonitoring(self.obdCommand, self.tick)

    def stopReadings(self):
        self.obdMonitor.stopMonitoring(self.obdCommand)



class Gauge_RPM(Gauge):
    obdCommand = obd.commands.RPM

    def __init__(self, monitor):
        super(Gauge_RPM, self).__init__(self.obdCommand, monitor)


    def processReading(self, reading):
        print(reading.value);


class Gauge_Speed(Gauge):
    obdCommand = obd.commands.SPEED

    def __init__(self, monitor):
        Gauge.__init__(self, self.obdCommand, monitor)


    def processReading(self, reading):
        print(reading.value);

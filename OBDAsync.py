import obd
import json
import syslog


class OBDAsyncConnector:
    obdConnection = None
    port = None

    def __init__(self, port):
        self.port = port

    def __init__(self):
        with open('config/connector.json') as cj:
            configData = json.load(cj)
            if configData['port']:
                self.port = configData['port']
            else:
                syslog.syslog(syslog.LOG_ERR, 'port not found in connector.json')

    def connect(self):
        if self.port:
            self.obdConnection = obd.Async(self.port)
        else:
            syslog.syslog(syslog.LOG_ERR, 'connect called with no port')

    def getConnection(self):
        return self.obdConnection

    def isConnectedToELM(self): # connected to ELM
        return self.obdConnection.status() == OBDStatus.ELM_CONNECTED

    def isIngitionOff(self):    # connected to OBD only
        return self.obdConnection.status() == OBDStatus.OBD_CONNECTED

    def isIngitionOn(self):     # fully connected
        return self.obdConnection.status() == OBDStatus.CAR_CONNECTED

    def isConnected(self): # same as above
        return self.obdConnection.is_connected()
    

    def getPort(self):
        return self.port


    def disconnect(self):
        self.obdConnection.close()

    

class OBDAsyncMonitor:
    obdAsyncConnection = None
    obdConnection = None


    def __init__(self, asyncConnection):
        self.obdAsyncConnection = asyncConnection
        self.obdConnection = self.obdAsyncConnection.getConnection()

    def start(self):
        if not self.obdConnection.running:
            self.obdConnection.start()

    def stop(self):
        if self.obdConnection.running:
            self.obdConnection.stop()

    def finish(self):
        with self.obdConnection.paused() as was_running:
            self.obdConnection.unwatch_all()

    def startMonitoring(self, command, callback):
        with self.obdConnection.paused() as was_running:
            self.obdConnection.watch(command, callback)

    def stopMonitoring(self, commnad, callback=None):
        with self.obdConnection.paused() as was_running:
            self.obdConnection.unwatch(command, callback)

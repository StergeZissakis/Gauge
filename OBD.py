import obd
import json
import syslog

class Connector:
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
        obdConnection = obd

    def getPort(self):
        return self.port

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
    
    def disconnect(self):
        self.obdConnection.close()

class OBDConnector(Connector):
    def connect(self):
        if self.port:
            self.obdConnection = obd.OBD(portstr=self.port)
            return self.obdConnection is not None
        else:
            syslog.syslog(syslog.LOG_ERR, 'connect called with no port')
            return False

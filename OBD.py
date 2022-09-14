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

    def getPort(self):
        return self.port

    def isConnected(self): # same as above
        return self.obdConnection.is_connected()
    
    def disconnect(self):
        self.obdConnection.close()

class OBDConnector(Connector):
    def connect(self):
        if self.port:
            self.obdConnection = obd.OBD(self.port)
            #obd.logger.setLevel(obd.logging.DEBUG)
            return self.isConnected()
        else:
            syslog.syslog(syslog.LOG_ERR, 'connect called with no port')
            return False

    def reconnect(self):
        if self.isConnected():
            self.disconnect()
        return self.connect()

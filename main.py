from OBDAsync import *
from Gauge import *
import time

if __name__ == "__main__":
    asyncConnection = OBDAsyncConnector()
    asyncConnection.connect()
    monitor = OBDAsyncMonitor(asyncConnection)
    rpmGauge = Gauge_RPM(monitor)
    speedGauge = Gauge_Speed(monitor)

    if asyncConnection.isConnected():
        rpmGauge.startReadings()
        speedGauge.startReadings()
        
        monitor.start()
        time.sleep(60)
        monitor.stop()
        monitor.finish()
        asyncConnection.disconnect()


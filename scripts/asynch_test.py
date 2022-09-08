import obd
import time

connection = obd.Async("/dev/pts/7")

cmd = obd.commands.SPEED

def rpm(r):
    if not r.is_null():
        print(r.value)

connection.watch(cmd, callback=rpm)
connection.start()

time.sleep(60)
connection.stop()


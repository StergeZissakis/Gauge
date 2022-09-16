import os
import syslog
import time
import socket
from UIGauge import *
import time
import threading
import panel as pn
pn.extension('echarts')

OUTGOING_FIFO_NAME="/tmp/gui2gauge"
INCOMING_FIFO_NAME="/tmp/gauge2gui"

rpmGauge = GaugeRPM()
klmGauge = GaugeKLM()

row = pn.Row(klmGauge.gaugeUI, rpmGauge.gaugeUI)
gaugeBox = pn.WidgetBox(row)
gaugeBox.servable()

jobs = {}
jobs[rpmGauge.name] = rpmGauge
jobs[klmGauge.name] = klmGauge


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(bytes("+" + rpmGauge.toPacket(), 'ascii'), ("127.0.0.1", 5656))
sock.sendto(bytes("+" + klmGauge.toPacket(), 'ascii'), ("127.0.0.1", 5656))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 5657))    


def run():
    while True:
        buff = sock.recv(1024)
        for packet in buff.split(b'\0'):
            print(packet)
            cmd, value = packet.split(':')
            if jobs[cmd]:
                jobs[cmd].setValue(value)


threading.Thread(target=run).start()

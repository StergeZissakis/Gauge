import OBD
import queue
from threading import Thread, Lock
import time
import copy
import syslog
import copy
from pprint import pprint

class Job: # an OBD command and the response processor
    gauge = None
    response = None

    def __init__(self, gauge):
        self.gauge = gauge


class CommandDispatcher(Thread): # pops off its internal thread safe q into the OBD query
    q = queue.Queue()
    connector = None
    obdConnection = None
    responseQ = None

    def __init__(self, connector, consumer):
        super(CommandDispatcher, self).__init__()
        self.connector = connector
        self.obdConnection = connector.obdConnection
        self.responseQ = consumer

    def run(self):
        while True:
            while self.connector.isConnected() == False:
                self.connector.reconnect()
            job = self.q.get()
            job.response = self.obdConnection.query(job.gauge.obdCommand)
            self.responseQ.push(job)

    def dispatch(self, job):
        self.q.put(job)


class ResponseQ(Thread): # queus up responses from CommnadDispatch: consumer
    q = queue.Queue()

    def __init__(self):
        super(ResponseQ, self).__init__()

    def push(self, job):
        self.q.put(job)

    def run(self):
        while True:
            job = self.q.get()
            resp = job.response
            if resp and resp.value is not None and resp.value.magnitude is not None:
                job.gauge.processReading(resp)
            else:
                syslog.syslog(syslog.LOG_INFO, 'ResponseQ: OBD Command [' + str(job.gauge.obdCommand) + '] is unreadable')
                

class TimedJobList(Thread): # a group of job at a specific timeout
    jobQ = []
    lock = Lock()
    timeout = None #milliseconds
    jobDispatcher = None

    def __init__(self, timeout, dispatcher):
        super(TimedJobList, self).__init__()
        self.timeout = timeout
        self.jobDispatcher = dispatcher

    def register(self, job):
        with self.lock:
            self.jobQ.append(job)

    def deregister(self, command):
        with self.lock:
            for job in self.jobQ:
                if job.obdCommand == command:
                    self.jobQ.remove(job)
                    break

    def run(self):
        sleepTime = self.timeout / 1000
        while True:
            time.sleep(sleepTime)
            for job in self.jobQ:
                self.jobDispatcher.dispatch(job)


class TimedJobManager: # registry of TimeJobLists
    registry = {}

    def watch(self, timeout, job, dispatcher):
        if timeout in self.registry.keys():
            self.registry[timeout].register(job)
        else:
            tjl = TimedJobList(timeout, dispatcher)
            tjl.register(job)
            self.registry[timeout] = tjl
            tjl.start()

    def unwatch(self, timeout, command):
        if timeout in self.registry.keys():
            self.registry[timeout].deregister(command)

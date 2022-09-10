import OBD
import queue
from threading import Thread, Lock
import time
import copy
import syslog

class Job: # an OBD command and the response processor
    gauge = None

    def __init__(self):
        pass 

    def __init___(self, gauge):
        self.gauge = gauge


class QJob(Job): # a Job with a response
    response = None

    def __init__(self, job):
        self.gauge = job.gauge

class CommandDispatcher(Thread): # pops off its internal thread safe q into the OBD query
    q = queue.Queue()
    connector = None
    obdConnection = None
    responseQ = None

    def __init__(self, connection, consumer):
        super(CommandDispatcher, self).__init__()
        self.connector = connection
        self.obdConnection = connection.getConnection()
        self.responseQ = consumer

    def run(self):
        while True:
            qJob = self.q.get()
            while self.connector.isConnected() == False:
                self.connector.reconnect()
            qJob.response = self.obdConnection.query(qJob.gauge.obdCommand)
            self.responseQ.push(qJob)

    def dispatch(self, job):
        qJob = QJob(job)
        self.q.put(qJob)


class ResponseQ(Thread): # queus up responses from CommnadDispatch: consumer
    q = queue.Queue()

    def __init__(self):
        super(ResponseQ, self).__init__()

    def push(self, qJob):
        self.q.put(qJob)

    def run(self):
        while True:
            qJob = self.q.get()
            resp = qJob.response
            if resp and resp.value is not None and resp.value.magnitude is not None:
                qJob.gauge.processReading(resp)
            else:
                syslog.syslog(syslog.LOG_INFO, 'ResponseQ: OBD Command [' + str(qJob.gauge.obdCommand) + '] is unreadable')
                

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

    def deregister(self, job):
        with self.lock:
            self.jobQ.remove(job)

    def run(self):
        sleepTime = self.timeout / 1000
        while True:
            for job in self.jobQ:
                with self.lock:
                    self.jobDispatcher.dispatch(job)
            time.sleep(sleepTime)


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

    def unwatch(self, timeout, job):
        if timeout in self.registry.keys():
            self.registry.deregsiter(job)

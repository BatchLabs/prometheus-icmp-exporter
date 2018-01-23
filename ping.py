#!/usr/bin/env python
import re
import subprocess
import time

import yaml
from prometheus_client import Gauge, start_http_server

lineres = re.compile('(^.*\s+\:\s+)(.*\=.*%)(.*)')

def ping(targets):
    ret = {}    
    cmd = ['fping', '-q', '-s', '-c3' ]
    p = subprocess.Popen(' '.join(cmd)+' '+' '.join(targets), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = p.communicate()
    for line in res[1].split('\n'):
        if lineres.search(line):
            try:
                ret = handle(line, ret)
            except:
                ret = failhandle(line, ret)
    return ret

def failhandle(line, ret):
    host = lineres.search(line).groups()[0].replace(' ', '').replace(':', '').strip(' ')
    ret[host] = {}
    ret[host]['loss'] = "100"
    return ret

def handle(line, ret):
    host, loss, lat = lineres.search(line).groups()
    host = host.replace(' ', '').replace(':', '').strip(' ')
    loss = loss.replace('xmt/rcv/%loss = ', '').split('/')[2].replace('%', '')
    lat = lathandle(lat.replace(',', '').strip(' '))
    if host not in ret:
        ret[host] = {}
    ret[host]['loss'] = loss
    ret[host]['lat'] = lat
    return ret

def lathandle(lat):
    lat = lat.split(' = ')
    head = lat[0].split('/')
    tail = lat[1].split('/')
    lat = dict(zip(head, tail))
    return lat

def getconfig():
    try:
        with open("/etc/ping/hosts.yml", 'r') as stream:
            try:
                config=yaml.load(stream)
                return config
            except yaml.YAMLError as exc:
                print(exc)
                return False
    except:
        return False

def pingtargets(config):
    return ping(config['targets'])

if __name__ == '__main__':
    metrics=Gauge('ping', 'ping measurment', ['host', 'metric'])
    config = getconfig()
    start_http_server(port=1222, addr=config['ipconfig'])
    while True:
        pings = pingtargets(config) 

        for host in pings:
            if 'lat' in pings[host]:
                for metric, value in pings[host]['lat'].iteritems():
                    metrics.labels(host, metric).set(value)
            if 'loss' in pings[host]:
                metrics.labels(host, 'loss').set(pings[host]['loss'])

        time.sleep(2)

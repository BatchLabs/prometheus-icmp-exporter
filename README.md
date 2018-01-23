# Purpose
Provides a whitebox latency prometheus exporter, easy to manage via ansible. The python script uses fping to parallize ICMP probes. The docker runs permanently and sends 3 ICMP packets every 2 seconds on each host.

# Requirements

* `python-pip`
* `python-yaml`
* `fping`
* `prometheus-client`

# Build
## Docker
```bash
git clone $repo
    && cd $repo \
    && docker build -t ping . \
    && docker run -ti -p 1222:1222 -v $(pwd)/example.conf.yml:/etc/ping/hosts.yml ping
```

## Docker-compose

```bash
git clone $repo
    && cd $repo \
    && docker-compose build \
    && docker-compose up -d 
```

# Configuration

## Configuration file
```yaml
targets:
  - 8.8.8.8 # add as many host as you want
  - 9.9.9.9

ipconfig: 0.0.0.0 # the ipaddress to bind on, let it on 0.0.0.0 if you use the docker.
```

## Ansible template

```jinja
{{ ansible_managed}}
targets:
{%for host in groups['wantedgroup']%}
{%if 'ipaddress' in hostvars[host]%}
  - {{ hostvars[host]['ipaddress'] }}
{%else%}
  - {{ inventory_hostname }}
{%endif%}
{%endfor%}
ipconfig: {{ ansible_default_ipv4.address }}
```
# Results

```bash
$ docker-compose up -d
Starting ping ... 
Starting ping ... done
$ curl 127.0.0.1:1222
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 235905024.0
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 48435200.0
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1516712374.92
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 0.16
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 7.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1048576.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="2",minor="7",patchlevel="13",version="2.7.13"} 1.0
# HELP ping ping measurment
# TYPE ping gauge
ping{host="8.8.8.8",metric="min"} 26.0
ping{host="9.9.9.9",metric="avg"} 27.0
ping{host="8.8.8.8",metric="max"} 26.0
ping{host="9.9.9.9",metric="max"} 27.0
ping{host="9.9.9.9",metric="loss"} 0.0
ping{host="9.9.9.9",metric="min"} 27.0
ping{host="8.8.8.8",metric="loss"} 0.0
ping{host="8.8.8.8",metric="avg"} 26.0
```


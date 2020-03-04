Python version
```
Please make sure that you are using Python version 3.8
Centos: https://computingforgeeks.com/how-to-install-python-on-3-on-centos/
Ubuntu: https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/
```

Install service
```
python3.8 -m pip install influx-rp-generator
```

Create YAML config file for your retentions
You can find example of the file in this repository - rp_config.yaml
```
default_rp:
  name: 'autogen' \\ name of your default retention policy
  duration: '7d'  \\ for how long need to store data in this policy

custom_rp:
  - name: 'long_term' \\ name of new retention policy
    duration: '360d' \\ for how long need to store data in this policy
    aggregation: '5m' \\ aggregation period during getting data from default retention policy
```

Run Service with default settings:
```
export PATH_TO_RP_CONFIG=/full path to rp_config.yaml; influx-rp-generator
```

Change URL to InfluxDB inside Grafana Data Source:
```
URL = http://127.0.0.1:8080/influx
Where 127.0.0.1 is the IP address of the server where you installed influx-rp-generator
```

Existing environment variables:

|Variable name|Description|Default|
|---|---|---|
|INFLUXDB_URL|URL to InfluxDB server | http://127.0.0.1:8086 |
|INFLUXDB_USER|User who has access to InfluxDB|grafana|
|INFLUXDB_PASS|Password for the user|grafana|
|RP_CHECK_TIME|How often need to check and update retention policies and CQ (in seconds)|30|

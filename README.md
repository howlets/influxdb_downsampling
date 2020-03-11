Python version
```
Please make sure that you are using Python version 3.8
Centos: https://computingforgeeks.com/how-to-install-python-on-3-on-centos/
Ubuntu: https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/
```

Install and configure service
```
python3.8 -m pip install influx-rp-generator
```

Prepare YAML config file for your retentions
You can find default config in this directory - /opt/influx-rp-generator/rp_config.yaml
```
default_rp:
  name: 'autogen' \\ name of your default retention policy
  duration: '30d'  \\ for how long need to store data in this policy

custom_rp:
  - name: 'long_term' \\ name of new retention policy
    duration: '360d' \\ for how long need to store data in this policy
    aggregation: '5m' \\ aggregation period during getting data from default retention policy
```

Run Service with default settings (By default service will get configuration from /opt/influx-rp-generator/rp_config.yaml):
```
influx-rp-generator
```

Change URL to InfluxDB inside Grafana Data Source:
```
URL = http://127.0.0.1:8080/influx
Where 127.0.0.1 is the IP address of the server where you installed influx-rp-generator
```

Existing environment variables:

|Variable name|Description|Default|
|---|---|---|
|PATH_TO_RP_CONFIG|Location of retention config file | /opt/influx-rp-generator/rp_config.yaml |
|INFLUXDB_URL|URL to InfluxDB server | http://127.0.0.1:8086 |
|INFLUXDB_USER|User who has access to InfluxDB|grafana|
|INFLUXDB_PASS|Password for the user|grafana|
|RP_CHECK_TIME|How often need to check and update retention policies and CQ (in seconds)|30|

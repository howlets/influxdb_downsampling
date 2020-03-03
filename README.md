Install service
```
python3 setup.py install
```

Run Service with default settings:
```
influx-rp-generator
```

Run Service with custom settings:
```
export INFLUXDB_RP="{\"short_term\": \"1w_1m\"}"; influx-rp-generator
```

Environment variables:

|Variable name|Description|Default|
|---|---|---|
|INFLUXDB_URL|URL to InfluxDB server | http://127.0.0.1:8086 |
|INFLUXDB_USER|User who has access to InfluxDB|grafana|
|INFLUXDB_PASS|Password for the user|grafana|
|INFLUXDB_DEFAULT_POLICY|Default retention policy which you are using|autogen|
|INFLUXDB_RP|List of RP and continuous queries to create. Where long_term - name of the policy, 48w - duration of retention policy, 5m - aggregation period |"{\\"long_term\\": \\"48w_5m\\"}"|
|RP_CHECK_TIME|How often need to check and update retention policies and CQ (in seconds)|30|

Change DOC
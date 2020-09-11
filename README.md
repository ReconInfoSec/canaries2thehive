# canaries2thehive

Create alerts in [The Hive](https://github.com/TheHive-Project/TheHive) from your [Thinkst](https://thinkst.com/) Canary alerts, to be turned into Hive cases.

Simple Python flask app that runs as a web server, and accepts POST requests from your canaries notifications.

This script supports either a single instance of TheHive 3, or multiple organisations (leveraging multi tenancy feature) in TheHive 4.

```
git clone https://github.com/ReconInfoSec/canaries2thehive.git /opt/canaries2thehive
```

Get up and running:
* Configure SSL certificate paths in `app.py`, or remove all context lines if not using SSL
* Copy `init.d/canaries2thehive.service` to `/etc/systemd/system/canaries2thehive.service`
* Add your Hive API keys in JSON format to `/opt/canaries2thehive/app/keys.json` 
* Set your Hive URL in `config.py`: `HIVE_URL`
* **Optional**: `app/__init__.py`, configure any other IP, hash, URL, or filename fields in place of CanaryIP, SourceIP, and CanaryName to include them as artifacts/observables in your alert

```
pip3 install -r requirements.txt
cp init.d/canaries2thehive.service /etc/systemd/system/
systemctl enable canaries2thehive 
systemctl start canaries2thehive
```

* Runs at https://0.0.0.0:5000, accepts POST requests
  * Point your Canary webhook to `https://[YOURSERVER].com:5000/create_alert`

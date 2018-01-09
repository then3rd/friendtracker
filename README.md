Copy example to example.ini and edit the config file to include your fb username and password
```
cp config{_example,}.ini
```

Basice environment config:
```
python3 -m venv venv
venv/bin/pip install -r requirements.txt
chmod +x tracker.py
```
Usage:
```
usage: tracker.py [-h] [--password] [--username [USERNAME]]
                  [--profile [PROFILE]] [--interval INTERVAL] [--total TOTAL]
                  [--interactive]

FB friend online status data agregation utility

optional arguments:
  -h, --help            show this help message and exit
  --password, -p        Prompt for interactive password, ignoring INI
  --username [USERNAME], -u [USERNAME]
                        Specify username, ignoring INI
  --profile [PROFILE], -r [PROFILE]
                        Specify account name, ignoring INI
  --interval INTERVAL, -v INTERVAL
                        Set interval time (minutes), ignoring INI
  --total TOTAL, -t TOTAL
                        Prompt for total time (hours), ignoring INI
  --interactive, -i     Run interactively instead of headless, ignoring INI
```

Run without any options to use config:
```
./tracker.py
```

Specify optional flags to override options from config:
```
./tracker.py -u foo@bar.com -r FooBar -v 1 -t 24 -i -p
```

Results:
```
[~/repos/friendtracker]$ ./tracker.py
1440.0 interations within 24.0 hrs total time @ 1.0 min interval
Logging into fb...
username sent
password sent
no disable notification popup detected at login
2 users online: Foo Bar, John Doe, Screenshot saved: screenshot1.png

Waiting for update
```

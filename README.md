Copy example to example.ini and edit the config file to include your fb username and password
```
cp config{_example,}.ini
```

Run it:
```
python3 -m venv venv
venv/bin/pip install -r requirements.txt
chmod +x tracker.py
./tracker.py
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

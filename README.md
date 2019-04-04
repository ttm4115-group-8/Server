# TTM4115 Group 8 - Server

## Start server on RPI: 

Go to the server folder:
```
cd ~/Development/ttm4115-group-8/Server/src/
```

Activate python 3 environment:
```
source ~/Development/py3/bin/activate
```
Start the server:
```
python server.py
```


## Access DB and view tables:
Connect to the DB
```

sqlite3 quickstart_app.sqlite

```

display tables

```
.tables
```

Show table scheme
```
.schema users
```

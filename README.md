# GeoIPs

[VirtualEnv Tutorial](https://docs.python.org/3/tutorial/venv.html)

## Installation (After cloning repo)

## Step 1

Have virtualenv installed with an environment activated in a terminal. After activating the environment, point to the root folder of the django application (manage.py is visible from here).


## Step 2

Run the following command to install dependencies:

```
pip install -r requirements.txt
```

## Step 3

3) Once the packages are installed navigate to the root folder of the project where you will see a file named 'manage.py'. In the terminal, run the command:

```
python manage.py runserver
```

The terminal should display something similar to:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 09, 2021 - 22:44:45
Django version 3.2.8, using settings 'IpTracker.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```


## Step 4

Open a browser and navigate to http://127.0.0.1:8000
Here you will see a JSON object displaying "data": "No IPs in memory"

The following endpoints are available (don't forget trailing /):

Returns all IP/Info in cache memory.
http://127.0.0.1:8000

Returns IP address along with name and country of origin.
http://127.0.0.1:8000/geo/api/{IP address}/

Returns a filtered list of IP address in the cache.
http://127.0.0.1:8000/geo/api/filter/{country or city name}/

Returns all IP/Info in cache memory in sorted order. If value is not 'city', then
list will be sorted by country.
http://127.0.0.1:8000/geo/api/sort/{'country' or 'city'}/

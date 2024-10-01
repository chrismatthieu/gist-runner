# Script Runner

Run bash and python scripts via a URL. These scripts run in a new thread and CLI returns the PID so that you can stop the process as needed by running:

````
kill -9 PID
````

You can also pass parameters after the URL as well as --help or --version

Examples:

BASH

````
./script_run https://gist.githubusercontent.com/chrismatthieu/946633097c70a521f955e3257bb58a6c/raw/7fe5e9d92adcaf88be45c7c70786e3e98b4adab4/hello.sh
````

Python

````
./script_run https://gist.githubusercontent.com/chrismatthieu/c71b2d223f166c2c4f58b0ac7c05b71b/raw/ac13e97814d61b31a99e458cdada5671452b2979/hello.py
````

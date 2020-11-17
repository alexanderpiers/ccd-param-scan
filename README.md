# ccd-param-scan
Takes images over a scan of a ccd voltage, clock or other parameter. Useful in optimizing or exploring a CCD parameter without having to manually change every setting. 

## Requirements
This code uses Python3 and the packages listed in the `requirements.txt`. Additionally this is a wrapper that executes CCDDrone, so CCDDrone must be installed.

To setup, run:

```
virtualenv env --python=python3 # creates virtual environment in ./env/
pip install -r requirements.txt # installs packages
source env/bin/activate # activates the environmnet
```


## Usage

To perform a parameter scan execute:

```
python parameterScan.py -s <parameter-scan>
```

The code takes in the following command line arguments:
```
-s --scan <parameter-scan> [REQUIRED]
-o --output <output-directory>
-d --drone <ccddrone-directory>
-c --config <base-config-filename>
-v --verbose
-h --help
```

The parameter scan is in the form:
```
--scan name start stop increment
```
You can repeat the name, star, stop, increment pattern to scan over multiple parameters, but you must always include all arguments.

For example, usage may look like:

```
python parameterScan.py -v -d /home/apiers/CCDDrone -c config/test-config.ini -s two_og_lo -10 -8 0.5 to_og_hi -2 2 1
```

To scan over `two_og_lo` and `two_og_hi`.


You can edit the defaults (for example the CCDDrone directory will be unique for each user, but likely not change) in the `parameterScan.py` file. 

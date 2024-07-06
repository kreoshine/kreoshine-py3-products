# DEVELOPMENT NOTES

## How to start

Clone the project
```bash
git clone git@github.com:kreoshine/kreoshine-py3-products.git
```

Change working directory
```bash
cd kreoshine-py3-products
```

Then there is a need to create environment-mode for dynaconf in '.env' file
``` bash
echo 'export KREOSHINE_ENV=DEVELOPMENT' >settings/config/.env
```

Create python virtual environment (with pip support, e.g. 'venv' or via 'conda')
and perform command:
``` bash
pip install -e .
```

Start environment in Docker (version >=1.5-2)
``` bash
start_dev_environment_in_background
```

Now application can be started:
``` bash
start
```

## How to build

Sure that your environment with 'build'
``` bash
pip install build
```

Build dist:
``` bash
python -m build
```

#### Note: settings should have all necessary files (such as '.env' and etc.)!
# DEVELOPMENT NOTES

## How to start

- Clone the project
```bash
git clone git@github.com:kreoshine/kreoshine-py3-products.git
```

- Change working directory
```bash
cd kreoshine-py3-products
```

- Create python virtual environment (with pip support, e.g. 'venv' or via 'conda')

After environment preparation install requirements with fixed version
``` bash
pip install -e .
```
and install test requirements:
``` bash
pip install -r requirements-test.txt
```

finally, perform development deployment
``` bash
perform_dev_deploy
```

#### notes:

- Docker should be installed on the machine (version >=1.5-2) with available docker-compose

#### separated manual commands (bash):
- _dev__up_docker_environment
- _dev__initialize_database
- _dev__start

## Database naming convention
- Use underscore_names instead of CamelCase
- Table names should be singular
- Short id fields (id instead of item_id)
- Don't use ambiguous column names
- Try to name foreign key columns the same as the columns they refer to

### Creation new revisions
- manually (sure that CWD is 'PROJECT_ROOT_PATH/db')
```bash
alembic -n 'public' revision --message 'message string to use with revision'
```
Note: prefer to make ordered versions for revisions (oldest at the end)

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
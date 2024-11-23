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

Start dev environment
``` bash
_dev__up_docker_environment
```
Note: Docker version >=1.5-2

``` bash
_dev__initialize_database
```

Now application can be started:
``` bash
_dev__start
```

## Database naming convention
- Use underscore_names instead of CamelCase
- Table names should be plural
- Spell out id fields (item_id instead of id)
- Don't use ambiguous column names
- Try to name foreign key columns the same as the columns they refer to

explanation [why](https://dev.to/ovid/database-naming-standards-2061)

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
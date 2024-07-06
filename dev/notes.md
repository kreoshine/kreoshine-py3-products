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

## Database naming convention
- Use underscore_names instead of CamelCase
- Table names should be plural
- Spell out id fields (item_id instead of id)
- Don't use ambiguous column names
- Try to name foreign key columns the same as the columns they refer to

explanation [why](https://www.baeldung.com/sql/database-table-column-naming-conventions)

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
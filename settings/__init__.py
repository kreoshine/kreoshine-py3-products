"""
Dynaconf app configuration

For more info see:
https://www.dynaconf.com/configuration/#available-options — about options of settings
"""
import os
from pathlib import Path

from dynaconf import LazySettings, Validator

PROJECT_ROOT_PATH = Path(os.path.abspath(__file__)).parents[1]

config = LazySettings(
    root_path=Path(os.path.abspath(__file__)).parent,

    settings_files=[
        'config/app.toml',
        'config/db.toml',
        'config/deploy.toml',
        'config/logging.toml',
    ],
    environments=True,  # activate multi-layered environments ([default], [development], [production])
    merge_enabled=True,  # allow to merge settings (e.g. from [default] layer)

    load_dotenv=True,  # read a '.env' file
    env_switcher='KREOSHINE_ENV',  # set variable name for applying environment
    envvar_prefix='KREOSHINE',  # all environment variables start with this prefix
    validators=[
        Validator("app.port", gt=1024),
        Validator("app.host", eq="127.0.0.1"),
        Validator("app.endpoints.products", eq="/products", env='PRODUCTION'),
    ]
)

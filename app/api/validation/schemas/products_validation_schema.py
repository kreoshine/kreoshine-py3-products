"""
Validation for 'products' view
"""
from app.api import const

PRODUCTS_QUERY_PARAMS__GET__SCHEMA = {
    const.query.keys.FIELDS: {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'string',
            'allowed': [
                const.query.values.TYPE,
                const.query.values.NAME,
            ]
        }
    },
}

"""
Validation schemas
"""
from app.api import const

QUERY_PARAMS_SCHEMA__GET_PRODUCTS = {
    const.query.keys.FIELDS: {
        # normalization
        'coerce': 'to_list_from_comma_separated_string',

        # validation
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

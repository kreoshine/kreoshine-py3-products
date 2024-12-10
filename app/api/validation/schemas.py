"""
Validation schemas
"""
from app.api import const

QUERY_PARAMS_VALIDATION_SCHEMA__GET_PRODUCTS = {
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
                const.query.values.PRODUCT_ID,
            ]
        }
    },
}

NORMALIZATION_SCHEMA__PRODUCT = {
    const.query.values.PRODUCT_ID: {
        'coerce': 'to_string_from_uuid',
        'type': 'string',
    },
    const.query.values.TYPE: {
        'type': 'string',
    },
    const.query.values.NAME: {
        'type': 'string',
    },
}

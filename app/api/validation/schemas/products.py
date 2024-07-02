"""
Validation for 'products' view
"""
from app import const

GET_PRODUCTS_QUERY_PARAMS_SCHEMA = {
    const.api.query.FIELDS: {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'string',
            'allowed': [
                const.api.product.TYPE,
                const.api.product.NAME,
            ]
        }
    },
}

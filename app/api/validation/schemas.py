"""
Validation schemas
"""
from app.api import const
from db.models import Product

QUERY_PARAMS_VALIDATION_SCHEMA__GET_PRODUCTS = {
    const.query.keys.FIELDS: {
        # normalization
        'coerce': 'to_list_from_comma_separated_string',

        # validation
        'type': 'list',
        'required': True,
        'unique_items': True,
        'schema': {
            'type': 'string',
            'coerce': 'to_snake_from_camel',
            'allowed': list(Product.metadata.tables['products'].columns.keys())
        }
    },
}

RESPONSE_JSON__NORMALIZATION_STRUCTURE__PRODUCTS = {
    # note: this is invalid schema and may be used only for custom normalization
    'type': 'list',
    'schema': {
        'type': 'dict',
        'keysrules': {
            'type': 'string',
            'coerce': 'to_camel_from_snake',
        },
        'schema': {
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
    }
}

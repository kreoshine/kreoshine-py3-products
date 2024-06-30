"""
todo
"""
from typing import List, Optional

PRODUCTS_DATA = [
    {
        'type': 'default',
        'name': 'KreoShine',
        'images_data': [
            {
                'url': '/static/images/logo.svg',
                'title': 'KreoShine',
            },
        ],
        'descriptions_content': [
            'Lorem the best',
            'agdsh328',
        ],
    }
]


class DAOProducts:
    """ Data access object for products """

    async def get_list_by_filter(
            self,
            # filters: Iterable[dict] = (),
            # order: Iterable[dict] = (),
            # limit: Optional[int] = None,
            # offset: Optional[int] = None,
            requested_fields: Optional[List[str]] = None,
    ) -> List[dict]:
        """ todo """
        result = []
        for product_data in PRODUCTS_DATA:
            product_info = {}
            for product_field, value in product_data.items():
                if requested_fields is not None and product_field in requested_fields:
                    product_info[product_field] = value
            result.append(product_info)
        return result

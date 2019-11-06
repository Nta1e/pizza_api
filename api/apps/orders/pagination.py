from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "limit"
    page_query_param = "page"

    def get_paginated_response(self, data):
        """
        returns a paginated response
        :param data:
        :return: paginated response
        """
        return Response(
            {
                "paginationMeta": {
                    "currentPage": self.page.number,
                    "currentPageSize": self.page_size,
                    "totalPages": self.page.paginator.num_pages,
                    "totalRecords": self.page.paginator.count,
                },
                "rows": data,
            }
        )

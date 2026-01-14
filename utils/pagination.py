from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for Movies Explorer API.

    Features:
    - Default page size = 10
    - Clients can set page size via `?page_size=` (max 50)
    - Returns extra metadata in a clean, user-friendly format
    - Supports backward and forward navigation URLs
    """

    page_size = 10
    page_size_query_param = 'page_size'  
    max_page_size = 50
    page_query_param = 'page'             

    def get_paginated_response(self, data):
        return Response({
            "status": "success",
            "pagination": {
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "next_page": self.get_next_link(),
                "previous_page": self.get_previous_link(),
                "page_size": self.get_page_size(self.request),
            },
            "results": data
        })

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        # aqui uso uma proteção para caso page seja none
        if not hasattr(self, "page") or self.page is None:
            return Response({
                "success": True,
                "data": data,
                "meta": {
                    "page": 1,
                    "total_pages": 1,
                    "total_items": len(data),
                }
            })

        return Response({
            "success": True,
            "data": data,
            "meta": {
                "page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "total_items": self.page.paginator.count,
            }
        })
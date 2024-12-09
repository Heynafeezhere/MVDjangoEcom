from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomOrderItemListPagination(PageNumberPagination):
    page_size = 5  # Default number of results per page
    page_size_query_param = 'page_size'  # Allows client to specify the page size (e.g., ?page_size=20)
    max_page_size = 100  # Maximum allowed page size
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Total count of items
            'next': self.get_next_link(),  # URL for the next page of results
            'previous': self.get_previous_link(),  # URL for the previous page of results
            'results': data  # The actual data for the current page
        })

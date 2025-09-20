
from rest_framework.pagination import PageNumberPagination	# pagination class for paginating large querysets 	
class DefaultPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allow client to set the page size using this query parameter
    max_page_size = 100  # Maximum limit for page size to prevent excessive data load


    
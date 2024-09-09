from rest_framework.pagination import CursorPagination

class ProductPagination(CursorPagination):
    page_size = 50
    ordering = '-created_at'  # 최신순 정렬
    cursor_query_param = 'page'
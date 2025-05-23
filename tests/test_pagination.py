from rest_framework.test import APIRequestFactory

from dj_rest_kit.pagination import CustomPagination


def test_paginate_queryset_limit_offset():
    factory = APIRequestFactory()
    request = factory.get('/', {'limit': 2, 'offset': 0})
    paginator = CustomPagination()
    data = list(range(5))
    page = paginator.paginate_queryset(data, request)
    assert page == data[:2]


def test_paginate_queryset_all():
    factory = APIRequestFactory()
    request = factory.get('/', {'limit': 'all'})
    paginator = CustomPagination()
    data = list(range(5))
    page = paginator.paginate_queryset(data, request)
    assert page == data


def test_paginate_queryset_offset_beyond_length():
    factory = APIRequestFactory()
    request = factory.get('/', {'limit': 2, 'offset': 10})
    paginator = CustomPagination()
    data = list(range(5))
    page = paginator.paginate_queryset(data, request)
    assert page == []

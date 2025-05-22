# dj-rest-kit

dj-rest-kit provides a set of utilities and base classes to speed up building REST APIs with [Django REST Framework](https://www.django-rest-framework.org/). It includes view mixins, serializer helpers, a custom renderer, pagination class and useful helper functions which are commonly needed across projects.

## Installation

Install the package from PyPI:

```bash
pip install dj-rest-kit
```

Add `dj_rest_kit` to your Django `INSTALLED_APPS` and import the components you need.

## Example usage

Use the provided viewsets and renderer to create consistent API responses:

```python
from rest_framework import routers
from dj_rest_kit.views import BaseViewSet
from dj_rest_kit.renderer import CustomRenderer

class BookViewSet(BaseViewSet):
    renderer_classes = [CustomRenderer]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    model = Book

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
```

The snippet above defines a simple `BookViewSet` using the base classes from
`dj_rest_kit`. It automatically handles list, create, retrieve, update and
delete operations while returning responses rendered by `CustomRenderer`.

Below is a more complete example including a serializer and pagination:

```python
# serializers.py
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

# views.py
from rest_framework.routers import DefaultRouter
from dj_rest_kit.views import BaseViewSet
from dj_rest_kit.renderer import CustomRenderer
from dj_rest_kit.pagination import CustomPagination

class BookViewSet(BaseViewSet):
    renderer_classes = [CustomRenderer]
    pagination_class = CustomPagination
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    model = Book

router = DefaultRouter()
router.register("books", BookViewSet)

```

You can also use the helper utilities anywhere in your project:

```python
from dj_rest_kit.helpers import generate_random_otp

otp = generate_random_otp()
print(otp)  # 6 digit one-time password
```

## Provided utilities

### Mixins

`dj_rest_kit.mixins` supplies a `ViewSetMixin` used by all base viewsets. It sets default authentication requirements, updates objects with the current user on save and exposes utility methods like `custom_error_response` for consistent error handling and `get_choices_for_model_fields` to expose model choice fields.

### Renderer

`CustomRenderer` formats API responses so that successful responses include `success`, `message`, `status` and `results` keys. Errors are wrapped in a similar structure for easier consumption by clients.

### Pagination

`CustomPagination` extends DRF's `LimitOffsetPagination` and supports a special `?limit=all` query that returns the entire dataset. It exposes the usual `count`, `next`, `previous` and `results` fields in the response.

### Helper utilities

`dj_rest_kit.helpers` contains miscellaneous functions, including:

- `get_response_message` – build success messages from serializer data
- `remove_null_key_value_pair` – strip empty values from dictionaries
- Date and time helpers to format or convert between user timezones and UTC
- `generate_random_otp` – produce a six digit one-time password
- `PathAndRename` – generate unique filenames for uploaded files

These helpers can be imported individually as needed.

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for details.

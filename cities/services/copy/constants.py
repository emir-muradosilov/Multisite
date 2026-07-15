from django.db import models


# Поля, которые никогда не копируем
SKIP_FIELDS = {
    "id",
    "pk",
    "created_at",
    "updated_at",
}


# Какие поля считаются текстовыми
TEXT_FIELD_TYPES = (
    models.CharField,
    models.TextField,
)
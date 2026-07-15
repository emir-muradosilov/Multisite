from .constants import (
    SKIP_FIELDS,
    TEXT_FIELD_TYPES,
)


def clone_model(
    instance,
    replacer=None,
    commit=True,
    **overrides,
):
    """
    Универсальное клонирование любой Django-модели.

    Копирует только обычные поля.

    ForeignKey копируются автоматически.

    ManyToMany не копируются.

    Parameters
    ----------

    replacer
        Экземпляр TextReplacer.

    commit
        Если False —
        объект НЕ сохраняется.

    overrides
        Любые поля,
        которые необходимо заменить.
    """

    model = instance.__class__

    values = {}

    for field in model._meta.fields:

        if field.name in SKIP_FIELDS:
            continue

        value = getattr(
            instance,
            field.name,
        )

        # автоматическая замена текста
        if (
            replacer
            and value
            and isinstance(field, TEXT_FIELD_TYPES)
        ):

            value = replacer.replace(
                value
            )

        values[field.name] = value

    values.update(
        overrides
    )

    new_instance = model(
        **values
    )

    if commit:

        new_instance.save()

    return new_instance
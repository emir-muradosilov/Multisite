import os
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.utils.text import slugify


def generate_seo_filename(
    title,
    city=None,
    extension='webp'
):

    parts = [title]

    if city:
        parts.append(city)

    filename = slugify(
        '-'.join(parts)
    )

    return f'{filename}.{extension}'


def convert_to_webp(
    image_field,
    quality=85
):

    if not image_field:
        return image_field

    img = Image.open(image_field)

    # RGB FIX
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    output = BytesIO()

    img.save(
        output,
        format='WEBP',
        quality=quality,
        optimize=True
    )

    output.seek(0)

    filename = os.path.splitext(
        image_field.name
    )[0]

    return ContentFile(
        output.read(),
        name=f'{filename}.webp'
    )
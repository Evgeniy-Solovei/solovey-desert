from django.utils.text import slugify

_CYRILLIC_TO_LATIN = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sch',
    'ъ': '',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
}


def slugify_title(title: str) -> str:
    transliterated = ''.join(
        _CYRILLIC_TO_LATIN.get(char, _CYRILLIC_TO_LATIN.get(char.lower(), char))
        for char in title.lower()
    )
    slug = slugify(transliterated)
    if slug:
        return slug
    return slugify(title, allow_unicode=True) or 'item'


def unique_slug_for_instance(instance, *, source_field='title', slug_field='slug'):
    source_value = getattr(instance, source_field, '') or ''
    base_slug = slugify_title(source_value)
    slug = base_slug
    counter = 1

    queryset = instance.__class__.objects.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.filter(**{slug_field: slug}).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1

    return slug


def ensure_slug_for_instance(instance, *, source_field='title', slug_field='slug'):
    source_value = getattr(instance, source_field, '') or ''
    current_slug = getattr(instance, slug_field, '') or ''

    if instance.pk:
        previous = (
            instance.__class__.objects
            .filter(pk=instance.pk)
            .values(source_field, slug_field)
            .first()
        )
        title_changed = previous is not None and previous[source_field] != source_value
    else:
        title_changed = False

    if not current_slug or title_changed:
        setattr(
            instance,
            slug_field,
            unique_slug_for_instance(instance, source_field=source_field, slug_field=slug_field),
        )

    return getattr(instance, slug_field)

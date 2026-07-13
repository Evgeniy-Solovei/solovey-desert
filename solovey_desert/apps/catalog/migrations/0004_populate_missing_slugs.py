from django.db import migrations


def populate_missing_slugs(apps, schema_editor):
    from apps.catalog.utils import unique_slug_for_instance

    for model_name in ('Category', 'Product'):
        model = apps.get_model('catalog', model_name)
        for instance in model.objects.filter(slug=''):
            instance.slug = unique_slug_for_instance(instance)
            instance.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_allow_blank_slug'),
    ]

    operations = [
        migrations.RunPython(populate_missing_slugs, migrations.RunPython.noop),
    ]

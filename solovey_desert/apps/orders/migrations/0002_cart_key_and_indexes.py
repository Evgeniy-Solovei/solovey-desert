import uuid

from django.db import migrations, models


def fill_cart_keys(apps, schema_editor):
    Cart = apps.get_model('orders', 'Cart')
    for cart in Cart.objects.filter(key__isnull=True):
        cart.key = uuid.uuid4()
        cart.save(update_fields=['key'])


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='key',
            field=models.UUIDField(null=True, editable=False, verbose_name='Постоянный ключ корзины'),
        ),
        migrations.RunPython(fill_cart_keys, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='cart',
            name='key',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name='Постоянный ключ корзины'),
        ),
        migrations.AddIndex(
            model_name='cart',
            index=models.Index(fields=['key'], name='orders_cart_key_1b8da8_idx'),
        ),
        migrations.AddIndex(
            model_name='cart',
            index=models.Index(fields=['updated_at'], name='orders_cart_updated_c19f83_idx'),
        ),
        migrations.AddIndex(
            model_name='cartitem',
            index=models.Index(fields=['cart', 'updated_at'], name='orders_cart_cart_id_373e09_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['status', '-created_at'], name='orders_orde_status_079368_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['phone'], name='orders_orde_phone_7bc88b_idx'),
        ),
    ]

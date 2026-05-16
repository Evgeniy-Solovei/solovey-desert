from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['is_active', 'order'], name='catalog_cat_is_acti_7b2d26_idx'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['is_featured', 'order'], name='catalog_cat_is_feat_97710c_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_active', 'order'], name='catalog_pro_is_acti_63ae7f_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_featured', 'order'], name='catalog_pro_is_feat_7a3833_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category', 'is_active', 'order'], name='catalog_pro_categor_0b9037_idx'),
        ),
        migrations.AddIndex(
            model_name='productimage',
            index=models.Index(fields=['product', 'order'], name='catalog_pro_product_631828_idx'),
        ),
        migrations.AddIndex(
            model_name='productweightoption',
            index=models.Index(fields=['product', 'order'], name='catalog_pro_product_73e9c8_idx'),
        ),
    ]

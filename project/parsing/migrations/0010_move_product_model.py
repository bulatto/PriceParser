from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0009_auto_20200411_1152'),
    ]

    database_operations = [
        migrations.AlterModelTable('Product', 'product_product'),

    ]

    state_operations = [
        migrations.DeleteModel('Product'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]

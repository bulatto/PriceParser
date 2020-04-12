from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0010_move_product_model'),
    ]

    database_operations = [
        migrations.AlterModelTable('Price', 'product_price'),

    ]

    state_operations = [
        migrations.DeleteModel('Price'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]

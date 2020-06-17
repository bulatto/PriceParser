from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0006_auto_20200216_1010'),
    ]

    operations = [
        migrations.RenameModel("Site", "Product")
    ]

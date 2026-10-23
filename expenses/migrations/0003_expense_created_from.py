from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_expenselimit'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='created_from',
            field=models.CharField(
                choices=[
                    ('manual', 'Manual Entry'),
                    ('voice_input', 'Voice Input'),
                    ('receipt_scan', 'Receipt Scan'),
                    ('api', 'API')
                ],
                default='manual',
                max_length=20
            ),
        ),
    ]

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoiceInputLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcript', models.TextField()),
                ('parsed_data', models.JSONField()),
                ('confidence', models.FloatField(default=0.8)),
                ('was_saved', models.BooleanField(default=False)),
                ('expense_id', models.IntegerField(blank=True, null=True)),
                ('income_id', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'verbose_name': 'Voice Input Log',
                'verbose_name_plural': 'Voice Input Logs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='VoiceCommand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('example', models.CharField(max_length=200)),
                ('category', models.CharField(default='expense', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'verbose_name': 'Voice Command',
                'verbose_name_plural': 'Voice Commands',
                'ordering': ['command'],
            },
        ),
        migrations.AddIndex(
            model_name='voiceinputlog',
            index=models.Index(fields=['user', '-created_at'], name='voice_featu_user_id_created_at_idx'),
        ),
    ]

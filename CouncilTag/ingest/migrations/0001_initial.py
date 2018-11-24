# Generated by Django 2.1.3 on 2018-11-24 04:43

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngageUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_time', models.PositiveIntegerField()),
                ('meeting_id', models.CharField(max_length=20, null=True)),
                ('processed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AgendaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('department', models.CharField(max_length=250)),
                ('body', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), default=list, size=None)),
                ('sponsors', models.CharField(max_length=250, null=True)),
                ('meeting_time', models.PositiveIntegerField(default=0)),
                ('agenda_item_id', models.CharField(max_length=20, null=True)),
                ('agenda', models.ForeignKey(on_delete='CASCADE', related_name='items', to='ingest.Agenda')),
            ],
        ),
        migrations.CreateModel(
            name='AgendaRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommendation', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=list, size=None)),
                ('agenda_item', models.ForeignKey(on_delete='CASCADE', related_name='recommendations', to='ingest.AgendaItem')),
            ],
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=250)),
                ('cutoff_offset_days', models.IntegerField(default=0)),
                ('cutoff_hour', models.PositiveIntegerField(default=11)),
                ('cutoff_minute', models.PositiveIntegerField(default=59)),
                ('location_tz', models.CharField(default='America/Los_Angeles', max_length=255)),
                ('location_lat', models.FloatField(default=34.024212)),
                ('location_lng', models.FloatField(default=-118.496475)),
            ],
        ),
        migrations.CreateModel(
            name='CommitteeMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=250)),
                ('lastname', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('committee', models.ForeignKey(on_delete='CASCADE', related_name='members', to='ingest.Committee')),
            ],
        ),
        migrations.CreateModel(
            name='EngageUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipcode', models.PositiveIntegerField(default=90401)),
                ('verified', models.BooleanField(default=False)),
                ('home_owner', models.BooleanField(default=False)),
                ('business_owner', models.BooleanField(default=False)),
                ('resident', models.BooleanField(default=False)),
                ('works', models.BooleanField(default=False)),
                ('school', models.BooleanField(default=False)),
                ('child_school', models.BooleanField(default=False)),
                ('authcode', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=254, null=True)),
                ('first_name', models.CharField(blank=True, max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, max_length=250, null=True)),
                ('zipcode', models.PositiveIntegerField(default=90401)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('home_owner', models.BooleanField(default=False)),
                ('business_owner', models.BooleanField(default=False)),
                ('resident', models.BooleanField(default=False)),
                ('works', models.BooleanField(default=False)),
                ('school', models.BooleanField(default=False)),
                ('child_school', models.BooleanField(default=False)),
                ('session_key', models.CharField(blank=True, max_length=100, null=True)),
                ('authcode', models.CharField(max_length=255, null=True)),
                ('date', models.PositiveIntegerField(default=0)),
                ('sent', models.PositiveIntegerField(default=0)),
                ('pro', models.PositiveIntegerField(default=0)),
                ('agenda_item', models.ForeignKey(null=True, on_delete='CASCADE', to='ingest.AgendaItem')),
                ('committee', models.ForeignKey(null=True, on_delete='CASCADE', to='ingest.Committee')),
                ('user', models.ForeignKey(null=True, on_delete='CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('icon', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='engageuserprofile',
            name='tags',
            field=models.ManyToManyField(to='ingest.Tag'),
        ),
        migrations.AddField(
            model_name='engageuserprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='agendaitem',
            name='tags',
            field=models.ManyToManyField(to='ingest.Tag'),
        ),
        migrations.AddField(
            model_name='agenda',
            name='committee',
            field=models.ForeignKey(on_delete='CASCADE', to='ingest.Committee'),
        ),
    ]

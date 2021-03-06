# Generated by Django 3.1.3 on 2020-11-27 00:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventapp', '0004_activity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imovel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inscricao_imobiliaria', models.CharField(blank=True, default='', max_length=255, null=True, unique=True)),
                ('codigo', models.IntegerField(unique=True)),
                ('matricula', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('razao_social', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('complemento', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('numero_contribuinte', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('fracao_ideal', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('zona', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('zona2012', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('filedatetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ImovelUpdateLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('total', models.IntegerField(default=0)),
                ('inalterados', models.IntegerField(default=0)),
                ('alterados', models.IntegerField(default=0)),
                ('novos', models.IntegerField(default=0)),
                ('response', models.CharField(blank=True, default='', max_length=255, null=True)),
            ],
            options={
                'ordering': ['-datetime'],
            },
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geometry_type', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('geometry_coordinates_json', models.TextField(blank=True, default='', null=True)),
                ('codigo', models.CharField(max_length=255, unique=True)),
                ('logradouro', models.CharField(max_length=255)),
                ('numero', models.CharField(default='S/N', max_length=255)),
                ('bairro', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('CEP', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('area_lote', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('filedatetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='NoticeColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('css_color', models.CharField(max_length=10, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ['date', 'id']},
        ),
        migrations.AlterModelOptions(
            name='notice',
            options={'ordering': ['date', 'id']},
        ),
        migrations.AlterModelOptions(
            name='noticeevent',
            options={'ordering': ['notice', 'notice_event_type', 'id']},
        ),
        migrations.AlterModelOptions(
            name='noticefine',
            options={'ordering': ['notice_event', 'date', 'id']},
        ),
        migrations.AlterModelOptions(
            name='surveyevent',
            options={'ordering': ['date', 'survey_event_type', 'id']},
        ),
        migrations.RenameField(
            model_name='noticeevent',
            old_name='end_concluded',
            new_name='concluded',
        ),
        migrations.RenameField(
            model_name='noticeeventtype',
            old_name='default_end_concluded',
            new_name='default_concluded',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='cnd_theme',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='demolicao_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='denuncia_cidadao_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='denuncia_mp_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='empresa_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='habitese_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='notice_deadline_infracao_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='notice_deadline_intimacao_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='notice_deadline_vistoria_administrativa_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='notice_embargo_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='notice_infracao_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='notice_infracao_embargo_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='notice_intimacao_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='notice_intimacao_embargo_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='notice_intimacao_infracao_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='notice_intimacao_infracao_embargo_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='obras_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='reforma_color',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='renovacao_color',
        ),
        migrations.AddField(
            model_name='noticeevent',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='noticeevent',
            name='report_number',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='noticeeventtype',
            name='css_color',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='noticeeventtype',
            name='show_concluded',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='noticeeventtype',
            name='show_deadline',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='noticeeventtype',
            name='show_fine',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='noticeeventtype',
            name='show_report_number',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='noticeeventtype',
            name='show_start',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='matricula',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='surveyeventtype',
            name='css_color',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activitys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='activity',
            constraint=models.UniqueConstraint(fields=('date', 'owner'), name='unique_per_day'),
        ),
        migrations.AddField(
            model_name='noticecolor',
            name='notice_event_types',
            field=models.ManyToManyField(to='eventapp.NoticeEventType'),
        ),
        migrations.AddField(
            model_name='imovel',
            name='lote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imoveis', to='eventapp.lote'),
        ),
        migrations.AddField(
            model_name='notice',
            name='imovel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notices', to='eventapp.imovel'),
        ),
        migrations.AddField(
            model_name='surveyevent',
            name='imovel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='survey_events', to='eventapp.imovel'),
        ),
    ]

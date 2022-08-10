# Generated by Django 2.2.2 on 2022-08-03 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否展示')),
                ('orders', models.IntegerField()),
                ('name', models.CharField(max_length=32, verbose_name='图片名字')),
                ('img', models.ImageField(help_text='图片尺寸必须是：3840*800', null=True, upload_to='banner', verbose_name='轮播图')),
                ('link', models.CharField(max_length=32, verbose_name='跳转连接')),
                ('info', models.TextField(verbose_name='图片简介')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

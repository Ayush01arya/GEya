# Generated by Django 3.2.2 on 2024-10-22 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ComplaintMS', '0006_auto_20241002_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='Type_of_complaint',
            field=models.CharField(choices=[('Can you help me understand the different career paths available for someone with my interests?', 'Can you help me understand the different career paths available for someone with my interests?'), ('What skills are most important for success in my desired career, and how can I develop them while still in school?', 'QWhat skills are most important for success in my desired career, and how can I develop them while still in school?'), ('What advice would you give me to stay motivated and focused on my career goals throughout my studies?', 'What advice would you give me to stay motivated and focused on my career goals throughout my studies?'), ('What are some common challenges people face in Engineering  career, and how can I prepare to handle them?', 'What are some common challenges people face in Engineering career, and how can I prepare to handle them?'), ('Other', 'Other')], max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]

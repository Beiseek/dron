from django.db import migrations, connection


def add_hero_image_column(apps, schema_editor):
    # Для SQLite добавляем колонку, если её нет
    with connection.cursor() as cursor:
        # Проверяем наличие колонки
        cursor.execute("PRAGMA table_info('landing_aboutblock');")
        columns = [row[1] for row in cursor.fetchall()]
        if 'hero_image' not in columns:
            # Добавляем простую колонку varchar(100); null допускается
            cursor.execute("ALTER TABLE landing_aboutblock ADD COLUMN hero_image varchar(100);")


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0013_merge_20251110_1157'),
    ]

    operations = [
        migrations.RunPython(add_hero_image_column, migrations.RunPython.noop),
    ]



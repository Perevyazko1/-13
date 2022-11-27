from django.core.management.base import BaseCommand, CommandError
from ...models import News, NewsCategory


class Command(BaseCommand):
    help = 'Подсказка вашей команды'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all products? yes/no')  # спрашиваем пользователя действительно ли он хочет удалить все товары
        answer = input(f'Вы хотите удалить все новости в категории {options["category"]} ')  # считываем подтверждение

        if answer != 'yes':  # в случае подтверждения действительно удаляем все товары
            self.stdout.write(self.style.EROR('Отменено.'))


        try:
            category = NewsCategory.objects.get(name=options['category'])
            News.object.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(
            f'Все новости в категории {category.name} успешно удалены'))  # в случае неправильного подтверждения

        except category.DoesNotExist:

            self.stdout.write(self.style.ERROR(f'Не удалось найти категорию {category.name}'))
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **options):
        # Получаем content type для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем или создаем разрешение can_unpublish_product
        can_unpublish, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может отменять публикацию продукта',
            content_type=content_type,
        )

        # Получаем разрешение на удаление продукта (создается автоматически)
        delete_product = Permission.objects.get(
            codename='delete_product',
            content_type=content_type,
        )

        # Создаем группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        group.permissions.add(can_unpublish, delete_product)
        group.save()

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует, права обновлены'))

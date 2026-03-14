from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cart.models import Product


class Command(BaseCommand):
    help = 'Seed the database with sample users and products'

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            id=1,
            defaults={
                'username': 'anand',
                'email': 'anand@example.com',
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username} (id={user.id})'))
        else:
            self.stdout.write(self.style.WARNING(f'User already exists: {user.username} (id={user.id})'))

        products_data = [
            {'id': 1, 'name': 'Wireless Mouse', 'price': 500.00},
            {'id': 2, 'name': 'Mechanical Keyboard', 'price': 1500.00},
            {'id': 3, 'name': 'USB-C Hub', 'price': 1000.00},
            {'id': 4, 'name': 'Monitor Stand', 'price': 800.00},
            {'id': 5, 'name': 'Webcam HD', 'price': 2000.00},
        ]

        for p_data in products_data:
            product, created = Product.objects.get_or_create(
                id=p_data['id'],
                defaults={
                    'name': p_data['name'],
                    'price': p_data['price'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name} (id={product.id}, price={product.price})'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.name} (id={product.id})'))

        self.stdout.write(self.style.SUCCESS('\nSeed data loaded successfully!'))

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import News, PostCategory, User
from .tasks import send_notifications


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribes: list[str] = []
        # users: list[str] = []
        for category in categories:
            subscribes += category.subscribes.all()
        # users = [s.username for s in subscribes]
        # subscribes = [s.email for s in subscribes]
        # print(users)
        # print(subscribes)
        send_notifications.delay(instance.id, instance.title, instance.text)


def send_new_user(user, email):
    html_content = render_to_string(
        'new_user.html',
        {
            'link': f'{settings.SITE_URL}/news/profile/',
            'user': user,
        }
    )
    message = EmailMultiAlternatives(
        subject='Регистрация',
        body='',  # это то же, что и message
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email,  # это то же, что и recipients_list

    )
    message.attach_alternative(html_content, 'text/html')  # добавляем html
    message.send()  # отсылаем


@receiver(post_save, sender=User)
def hello_new_user(sender, instance, created, **kwargs):
    if created:
        email = [instance.email]
        user = instance
        send_new_user(user, email)


@receiver(post_delete, sender=News)
def delete_post(sender, instance, **kwargs):
    id = instance.id
    cache.delete(f'news-{id}')


@receiver(post_save, sender=News)
def update_post(sender, instance, **kwargs):
    id = str(instance.id)
    cache.delete(f'news-{id}')

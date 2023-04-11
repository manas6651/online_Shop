from django.core.mail import send_mail


def order_data_sender_to_email(user, address, phone_number, message, products):
          send_mail(
            f'Заказ{user}',
            f'На Адрес{address}\nНомер телефона:{phone_number}\nСобшение:{message}\nТовар:{[i.title for i in products]}',
            'manas855.m08@gmail.com',
            ['manas6651@gmail.com'],
            fail_silently=False,
        )        
import threading

from django.core.mail import send_mail

from config import settings


class EmailThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        send_mail('e-shop', 'Поздравляем! Ваша статья достигла 100 просмотров!',
                  settings.EMAIL_HOST_USER, ['zasbox@mail.ru'])
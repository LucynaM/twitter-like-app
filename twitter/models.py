from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class ModelBasicInfo(models.Model):
    edited_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    banned = models.BooleanField(default=False)
    class Meta:
        abstract=True


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    @property
    def nick(self):
        return self.email[:self.email.index('@')].title()

    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"


class Tweet(ModelBasicInfo):
    content = models.TextField(max_length=400)
    user = models.ForeignKey(MyUser, related_name='entries', on_delete=models.CASCADE)

    def __str__(self):
        return '{}...'.format(self.content[:30])


class Comments(ModelBasicInfo):
    content = models.CharField(max_length=60, verbose_name='treść')
    user = models.ForeignKey(MyUser, related_name='comments', verbose_name='użytkownik')
    tweet = models.ForeignKey(Tweet, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return '{}...'.format(self.content[:30])

    class Meta:
        verbose_name = 'Komentarz'
        verbose_name_plural = 'Komentarze'


class Messages(models.Model):
    from_user = models.ForeignKey(MyUser, related_name='from_messages', verbose_name='od')
    to_user = models.ForeignKey(MyUser, related_name='to_messages', verbose_name='do')
    message = models.TextField(verbose_name='treść')
    is_read = models.BooleanField(default=False, verbose_name='przeczytana')
    created_at = models.DateTimeField(auto_now_add=True)
    banned = models.BooleanField(default=False)

    def __str__(self):
        return '{}...'.format(self.message[:30])

    class Meta:
        verbose_name = 'Wiadomość'
        verbose_name_plural = 'Wiadomości'


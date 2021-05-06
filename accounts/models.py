import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from .validators import validate_username
from django.utils.crypto import get_random_string


class User(AbstractUser):
    username = models.CharField(
        max_length=150, blank=False, null=False, unique=True, validators=[validate_username])
    email = models.EmailField(
        max_length=150, unique=True, blank=False, null=False)

    bio = models.CharField(max_length=50, default="")

    objects = UserManager()

    def content_from_file(instance, filename):
        name, ext = filename.split('.')

        file_path = 'avatar/{username}/'.format(
            username=instance.username)

        try:
            for f in os.listdir(file_path):
                os.remove(os.path.join(file_path, f))

        except OSError:
            pass

        random_string = get_random_string(length=32)

        file_path = 'avatar/{username}/avatar_{random_string}.{ext}'.format(
            username=instance.username,
            random_string=random_string,
            ext=ext
        )

        return file_path

    avatar = models.ImageField(
        upload_to=content_from_file, blank=True, null=True)

    @property
    def get_avatar(self):
        return f'/media/{self.avatar}'

    @property
    def get_anonymous_avatar(self):
        return f'/media/avatar/anonymous_avatar.png'

    @property
    def get_answers(self):
        answers = self.answers.filter(anonymous=False)
        return answers

    @property
    def get_questions(self):
        questions = self.questions.filter(anonymous=False)
        return questions

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

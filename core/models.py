from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class Question(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='questions')
    anonymous = models.BooleanField(default=False)
    content = models.TextField()
    upvotes = models.ManyToManyField(
        User, related_name='question_upvotes', blank=True)
    downvotes = models.ManyToManyField(
        User, related_name='question_downvotes', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def uploaded_on(self):
        uploaded_on = self.timestamp.date()
        timestamp_seconds = (datetime.now(timezone.utc) -
                             self.timestamp).total_seconds()

        if timestamp_seconds < 86400:
            if timestamp_seconds < 60:
                uploaded_on = "Just Now"
            elif timestamp_seconds < 3600:
                t = int(timestamp_seconds / 60)
                uploaded_on = f'{t} {"minute" if t == 1 else "minutes"} ago'
            else:
                t = int(timestamp_seconds / 3600)
                uploaded_on = f'{t} {"hour" if t == 1 else "hours"} ago'

        return uploaded_on

    @property
    def number_of_upvotes(self):
        return self.upvotes.all().count() - self.downvotes.all().count()

    def __str__(self):
        return f'{self.author.username}: {self.content}'


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='answers')
    anonymous = models.BooleanField(default=False)
    content = RichTextUploadingField()
    upvotes = models.ManyToManyField(
        User, related_name='answer_upvotes', blank=True)
    downvotes = models.ManyToManyField(
        User, related_name='answer_downvotes', blank=True)
    shares = models.ManyToManyField(
        User, related_name='answer_shares', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def uploaded_on(self):
        uploaded_on = self.timestamp
        timestamp_seconds = (datetime.now(timezone.utc) -
                             self.timestamp).total_seconds()

        if timestamp_seconds < 86400:
            if timestamp_seconds < 60:
                uploaded_on = "Just Now"
            elif timestamp_seconds < 3600:
                t = int(timestamp_seconds / 60)
                uploaded_on = f'{t} {"minute" if t == 1 else "minutes"} ago'
            else:
                t = int(timestamp_seconds / 3600)
                uploaded_on = f'{t} {"hour" if t == 1 else "hours"} ago'

        return uploaded_on

    @property
    def number_of_upvotes(self):
        return self.upvotes.all().count() - self.downvotes.all().count()

    def __str__(self):
        return f'{self.author.username}: {self.content}'


class AnswerComment(models.Model):
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    upvotes = models.ManyToManyField(
        User, related_name='comment_upvotes', blank=True)
    downvotes = models.ManyToManyField(
        User, related_name='comment_downvotes', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def uploaded_on(self):
        uploaded_on = self.timestamp
        timestamp_seconds = (datetime.now(timezone.utc) -
                             self.timestamp).total_seconds()

        if timestamp_seconds < 86400:
            if timestamp_seconds < 60:
                uploaded_on = "Just Now"
            elif timestamp_seconds < 3600:
                t = int(timestamp_seconds / 60)
                uploaded_on = f'{t} {"minute" if t == 1 else "minutes"} ago'
            else:
                t = int(timestamp_seconds / 3600)
                uploaded_on = f'{t} {"hour" if t == 1 else "hours"} ago'

        return uploaded_on

    @property
    def number_of_upvotes(self):
        return self.upvotes.all().count() - self.downvotes.all().count()

    def __str__(self):
        return self.content


class AnswerRequest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='requests')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answer_requests')
    request_list = models.ManyToManyField(
        User, related_name='answer_requests', blank=True)

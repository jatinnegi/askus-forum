from django.contrib import admin
from .models import Question, Answer, AnswerComment, AnswerRequest

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswerComment)
admin.site.register(AnswerRequest)

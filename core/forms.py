from django import forms
from .models import Answer, Question
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class QuestionForm(forms.ModelForm):
    content = forms.CharField(label="", required=True, widget=forms.Textarea(
        attrs={
            'class': "form-control",
            'onKeyUp': 'questionContentKeyUp(event)',
            'rows': "5",
            'placeholder': "Your question..."
        }
    ))

    anonymous = forms.BooleanField(
        required=False, initial=False, widget=forms.CheckboxInput(attrs={
            'id': 'question-form-anonymous',
            # 'class': 'form-check-input'
        }))

    class Meta:
        model = Question
        fields = ('content', 'anonymous', )


class AnswerForm(forms.ModelForm):
    content = forms.CharField(label="", widget=CKEditorUploadingWidget(
        attrs={'id': 'ckeditor_content', 'name': 'ckeditor_content'}
    ))

    anonymous = forms.BooleanField(
        required=False, initial=False, widget=forms.CheckboxInput(attrs={
            'id': 'answer-form-anonymous',
            # 'class': 'form-check-input'
        }))

    class Meta:
        model = Answer
        fields = ('content', 'anonymous', )

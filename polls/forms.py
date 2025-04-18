from django import forms
from polls.models import Question

class QuestionForm(forms.ModelForm):
    choice1 = forms.CharField(
        label='choice1',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    choice2 = forms.CharField(
        label='choice2',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Question
        fields = ['question_Text']  # 모델에서 가져올 필드는 질문 텍스트만
        labels = {
            'question_Text': '질문 제목',
        }
        widgets = {
            'question_Text': forms.TextInput(attrs={'class': 'form-control'}),
        }
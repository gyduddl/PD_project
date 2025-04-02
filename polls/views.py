from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Question, Choice

def index(request): # 메인 페이지
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    print("Latest Questions:", latest_question_list)
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id): # 상세 페이지
    question = get_object_or_404(Question, pk=question_id) # question_id에 해당하는 Question를 가져옴.없으면 404 페이지 반환
    print(f"Question ID: {question_id}, Question Text: {question.question_Text}")
    return render(request, 'polls/detail.html', {'question': question}) # polls/detail.html 템플릿을 렌더링하면서 question 객체 전달

def results(request, question_id): # 결과 페이지
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id): # 투표기능
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])#key, value값으로 데이터 받아옴
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('results', args=(question.id,)))

# def reset(request):
#     if request.method == "POST":
#         Choice.objects.update(votes=0)
#         return HttpResponse("All votes have been reset!")  # 또는 리디렉트
#     return HttpResponse("Invalid request", status=400)
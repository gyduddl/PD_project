from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.urls import reverse
from .models import Question, Choice
from django.utils import timezone

def index(request): # 메인 페이지
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id): # 상세 페이지
    question = get_object_or_404(Question, pk=question_id) # question_id에 해당하는 Question를 가져옴.없으면 404 페이지 반환
    choices = question.choice_set.all()
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

def reset(request, question_id): #리셋 버튼
    question = get_object_or_404(Question, pk=question_id)
    question.choice_set.update(votes=0)
    return HttpResponseRedirect(reverse('results', args=(question.id,)))

def likes(request, question_id): #좋아요 기능
    question = get_object_or_404(Question, pk=question_id)
    if question.like_users.filter(pk=request.user.pk).exists():
        question.like_users.remove(request.user)
    else:
        question.like_users.add(request.user)
    return HttpResponseRedirect(reverse('detail', args=(question.id,)))

def create(request):
    if request.method == "POST":
        question_Text = request.POST.get('title')
        choice1_text = request.POST.get('choice1')
        choice2_text = request.POST.get('choice2')
        user = request.user
        # 질문 생성
        question = Question.objects.create(
            user = user,
            question_Text = question_Text,
            pub_date = timezone.now()
        )

        # 선택지 생성
        Choice.objects.create(question=question, choice_text=choice1_text)
        Choice.objects.create(question=question, choice_text=choice2_text)

        return redirect('detail', question_id=question.id)
    return render(request, 'polls/index.html')
    
def delete(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    # 로그인한 유저가 작성자일 때만 삭제 허용 (보안)
    if request.user == question.user:
        question.delete()

    return redirect('index')  # 삭제 후 리디렉트할 페이지

def modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id) 
    return render(request, 'polls/modify.html', {'question': question}) 

def update(request, question_id):  
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.user:
        return HttpResponseForbidden("You are not authorized to edit this post.") 

    if request.method == 'POST':
            print(request.POST)
            question_Text = request.POST.get('title')
            choice1_text = request.POST.get('choice1')
            choice2_text = request.POST.get('choice2')

            question.question_Text =question_Text
            question.pub_date = timezone.now()

            choices = question.choice_set.all()

            if len(choices) >= 1:
                choices[0].choice_text = choice1_text  # 첫 번째 선택지 업데이트
                choices[0].save()

            if len(choices) >= 2:
                choices[1].choice_text = choice2_text  # 두 번째 선택지 업데이트
                choices[1].save()

            question.save()            

            return redirect('detail', question_id=question.id)
    return render(request, 'poll/modify.html', {'question': question})


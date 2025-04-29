from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.urls import reverse
from .models import Question, Choice
from django.utils import timezone
from .forms import QuestionForm

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
    choices = question.choice_set.all()
    total_votes = sum(choice.votes for choice in choices)
    choices_with_percentage = []
    for choice in choices:
        if total_votes > 0:
            percentage = (choice.votes / total_votes) * 100
        else:
            percentage = 0
        choices_with_percentage.append({
            'choice_text': choice.choice_text,
            'votes': choice.votes,
            'percentage': round(percentage, 2),  # 소수점 둘째 자리까지
        })
    return render(request, 'polls/results.html', {
        'question': question,
        'choices': choices_with_percentage,
        'total_votes': total_votes,
    })

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
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def reset(request, question_id): #리셋 버튼
    question = get_object_or_404(Question, pk=question_id)
    question.choice_set.update(votes=0)
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def likes(request, question_id): #좋아요 기능
    question = get_object_or_404(Question, pk=question_id)
    if question.like_users.filter(pk=request.user.pk).exists():
        question.like_users.remove(request.user)
    else:
        question.like_users.add(request.user)
    return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

def create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.pub_date = timezone.now()
            question.save()

            # choice1, choice2는 별도로 생성
            choice1_text = form.cleaned_data.get('choice1')
            choice1_image = form.cleaned_data.get('choice_1_img')
            choice2_text = form.cleaned_data.get('choice2')
            choice2_image = form.cleaned_data.get('choice_2_img')

            Choice.objects.create(question=question, choice_text=choice1_text, image=choice1_image)
            Choice.objects.create(question=question, choice_text=choice2_text, image=choice2_image)

            return redirect('polls:detail', question_id=question.id)
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'polls/new.html', context)
    
def delete(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    # 로그인한 유저가 작성자일 때만 삭제 허용 (보안)
    if request.user == question.user:
        question.delete()

    return redirect('polls:index')  # 삭제 후 리디렉트할 페이지

def modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id) 
    return render(request, 'polls/modify.html', {'question': question}) 

def update(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.user:
        return HttpResponseForbidden("You are not authorized to edit this post.")

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question.question_Text = form.cleaned_data.get('question_Text')
            question.pub_date = timezone.now()
            question.save()

            choice1_text = form.cleaned_data.get('choice1')
            choice1_image = form.cleaned_data.get('choice_1_img')
            choice2_text = form.cleaned_data.get('choice2')
            choice2_image = form.cleaned_data.get('choice_2_img')
            print(choice1_image)

            choices = question.choice_set.all().order_by('id')

            if len(choices) >= 1:
                choices[0].choice_text = choice1_text
                if choice1_image:
                    choices[0].image = choice1_image
                choices[0].save()

            if len(choices) >= 2:
                choices[1].choice_text = choice2_text
                if choice2_image:
                    choices[1].image = choice2_image
                choices[1].save()

            return redirect('polls:detail', question_id=question.id)
    else:
        # 처음 수정 화면 들어올 때, 기존 데이터 넣어주기
        initial_data = {
            'question_Text': question.question_Text,
        }
        choices = question.choice_set.all().order_by('id')
        if len(choices) >= 1:
            initial_data['choice1'] = choices[0].choice_text
        if len(choices) >= 2:
            initial_data['choice2'] = choices[1].choice_text

        form = QuestionForm(initial=initial_data)

    context = {'form': form, 'question': question}
    return render(request, 'polls/modify.html', context)



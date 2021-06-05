from django.shortcuts import render, redirect
from django.contrib.auth import forms, login, logout
from django.contrib.auth.decorators import login_required
from .models import Questao, Resposta, Poll
from .forms import RegisterUserForm, LoginForm, NewQuestionForm, NewResponseForm, NewReplyForm
# Create your views here.

def registerPage(request):
    form = RegisterUserForm()

    if request.method == 'POST':
        try:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                #login(request, user)
                return redirect('login')
        except Exception as e:
            print(e)
            raise

    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def loginPage(request):
    form = LoginForm()

    if request.method == 'POST':
        try:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('index')
        except Exception as e:
            print(e)
            raise

    context = {
        'form': form
    }

    return render(request, 'login.html', context)

@login_required(login_url='register')
def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def newQuestionPage(request):
    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.save()
                return redirect('question', question.id)
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'new-question.html', context)

def homepage(request):
    questions = Questao.objects.all().order_by('-created_at')
    polls = Poll.objects.all().order_by('-created_at')
    context = {
        'questions': questions,
        'polls': polls
    }
    return render(request, 'homepage.html', context)

@login_required(login_url='login')
def topicsPage(request):
    questions = Questao.objects.all().order_by('-created_at')
    context = {
        'questions': questions
    }
    return render(request, 'topics.html', context)    

@login_required(login_url='login')
def allpollsPage(request):
    polls = Poll.objects.all().order_by('-created_at')
    context = {
        'polls': polls
    }
    return render(request, 'poll-all.html', context)   

@login_required(login_url='login')
def questionPage(request, id):
    response_form = NewResponseForm()
    reply_form = NewReplyForm()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = request.user
                response.question = Questao(id=id)
                response.save()
                return redirect('/questao/'+str(id)+'#'+str(response.id))
        except Exception as e:
            print(e)
            raise

    question = Questao.objects.get(id=id)
    context = {
        'question': question,
        'response_form': response_form,
        'reply_form':  reply_form,
    }
    return render(request, 'question.html', context)

@login_required(login_url='register')
def replyPage(request):
    if request.method == 'POST':
        try:
            form = NewReplyForm(request.POST)
            if form.is_valid():
                question_id = request.POST.get('question')
                parent_id = request.POST.get('parent')
                reply = form.save(commit=False)
                reply.user = request.user
                reply.question = Questao(id=question_id)
                reply.parent = Resposta(id=parent_id)
                reply.save()
                return redirect('/questao/'+str(question_id)+'#'+str(reply.id))
        except Exception as e:
            print(e)
            raise
    return redirect('index')

@login_required(login_url='login')
def pollPage(request, id):
    poll = Poll.objects.get(id=id, pk=id)

    if request.method == 'POST':
        selected_option = request.POST.get('poll')
        if selected_option == 'option1':
            poll.option_one_count += 1;
        elif selected_option == 'option2':
            poll.option_two_count += 1;
        elif selected_option == 'option3': 
            poll.option_three_count += 1;
        
        poll.save()
        return redirect('results', poll.id)
    context = {
        'poll': poll
    }
    return render(request, 'poll.html', context)

@login_required(login_url='login')
def results(request, id):
    poll = Poll.objects.get(id=id, pk=id)

    context = {
        'poll' : poll
    }
    return render(request, 'results.html', context)
# from mainapp.models import Result, Test
from pprint import pprint
from unicodedata import name
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import environ
from pymongo import MongoClient
from datetime import date
from bson.objectid import ObjectId

env = environ.Env()
# reading .env file
environ.Env.read_env()

client = MongoClient(env('MONGO_CREDENTIAL'))
db = client['postuino-db-kjsceHack']

sessions = db['sessions']


def home_page(request):
    return render(request, 'mainapp/home.html', {'title': 'Home'})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.full_name = form.cleaned_data.get('full_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.height_cms = form.cleaned_data.get('height_cms')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'mainapp/register.html', {'form': form, 'title': 'Register'})


@login_required
def choose(request):
    return render(request, 'mainapp/choose.html', {'title':  'Choose', 'name': 'Mohil'})


@login_required
def session(request):
    if request.method == 'POST':
        session_details = {
            'user': request.user.id,
            'session_slouches': request.POST['slouches'],
            'session_startTime': request.POST['startTime'],
            'session_endTime': request.POST['endTime'],
            'session_date': request.POST['date'],
            'session_slouch_timeline': request.POST['slouchKeeper']
        }
        objId = sessions.insert_one(session_details).inserted_id
        return redirect('session-analysis', objId)
    name = request.user
    context = {
        'title': 'Session',
        'name': name
    }
    return render(request, 'mainapp/session.html', context)


def returnDayMonth(date):
    ans = []
    day = ''
    for i in range(len(date)):
        if date[i] == '-':
            ans.append(int(day))
            day = ''
        else:
            day += date[i]
    ans.append(int(day))
    return ans


@login_required
def analysis(request):
    filtered_sessions = sessions.find({'user': request.user.id})
    fsessions = []
    x, y, maxY = [], [], -1
    for session in filtered_sessions:
        ans = returnDayMonth(session['session_date'])
        x.append(session['session_date'])
        y.append(session['session_slouches'])
        maxY = max(maxY, int(session['session_slouches']))
        fsessions.append({
            'startTime': session['session_startTime'],
            'date': date(day=ans[2], month=ans[1], year=ans[0]).strftime('%d %B %Y'),
            'x': x,
            'y': y,
            'pk': session['_id']
        })
    context = {'title': 'Analysis',
               'name': request.user.profile.full_name,
               'sessions': fsessions,
               'x': x,
               'y': y,
               'maxY': maxY
               }
    return render(request, 'mainapp/analysis.html', context)


@login_required
def session_analysis(request, pk):
    info = sessions.find_one({'_id': ObjectId(pk)})
    print(info, pk)
    slouch_tl = eval(info['session_slouch_timeline'])
    print(slouch_tl)
    x, y, maxY = [], [], -1
    ans = returnDayMonth(info['session_date'])
    for i in slouch_tl:
        x.append(i[0])
        y.append(i[1])
        maxY = max(maxY, int(info['session_slouches']))
    context = {
        'x': x,
        'y': y,
        'date': date(day=ans[2], month=ans[1], year=ans[0]).strftime('%d %B %Y'),
        'no_slouches': info['session_slouches']
    }
    return render(request, 'mainapp/graph2.html', context)


# def graph(request):
#     return render(request, 'mainapp/graph.html')


# def graph2(request):
#     return render(request, 'mainapp/graph2.html')

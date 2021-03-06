from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *


def login(request):
    context = {}
    if request.method == 'POST':
        m = Admin.objects.get(adminuser=request.POST['adminuser'])
        if m.adminpass == request.POST['adminpass']:
            request.session['admin_id'] = m.adminid
            request.session['user'] = m.adminuser
            return redirect('/')
        else:
            context['fail'] = True
            return render(request, 'signin.html', context)
    else:
        context['field'] = AdminForm()
        return render(request, 'signin.html', context)


def logout(request):
    try:
        del request.session['admin_id']
        del request.session['user']
    except KeyError:
        pass
    return redirect('/')


def index(request):
    try:
        context = {}
        context['user'] = request.session['user']
        context['transactions'] = Transaction.objects.all().order_by('-datetime')
        return render(request, 'index.html', context)
    except KeyError:
        return redirect('/login')


def users(request):
    context = {}
    context['users'] = User.objects.all()
    return render(request, 'user.html', context)

def transact(request):
    context = {}
    context['transactions'] = Transaction.objects.all().order_by('-datetime')
    return render(request, 'transaction.html', context)

def transact_d(request):
    context = {}
    start_date = request.POST['start']
    end_date = request.POST['end']
    context['transactions'] = Transaction.objects.filter(datetime=(start_date, end_date)).order_by('-datetime')
    return render(request, 'transaction.html', context)


def transact_u(request, user_id):
    context = {}
    user = User.objects.get(uid=user_id)
    context['transactions'] = Transaction.objects.filter(userid=user).order_by('-datetime')
    return render(request, 'transaction.html', context)


def transact_med(request, med_id):
    context = {}
    context['transactions'] = Transaction.objects.filter(medid=med_id).order_by('-datetime')
    return render(request, 'transaction.html', context)


def medicine(request):
    context = {}
    context['medicines'] = Medicine.objects.all()
    return render(request, 'medicine.html', context)

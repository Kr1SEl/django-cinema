from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
import django.utils.timezone as tz
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Session, Hall, Cinema, Place
from .forms import SessionForm
from .filters import SessionFilter


def add_session(request):
    submitted = False
    if request.method == 'POST':
        form = SessionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            sessionId = form.save().pk
            numberOfPlaces = form.save().hall.sitPlaces
            for i in range(numberOfPlaces):
                place = Place(placeNumber=i+1, isAvaliable=True,
                              session=Session.objects.get(pk=sessionId))
                place.save()
            return HttpResponseRedirect('/add_session?submitted=True')
    else:
        form = SessionForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'cinemaApp/add_session.html', {'form': form, 'submitted': submitted})


# Todo make check for time
def my_tickets(request):
    if request.user.is_authenticated:
        tickets = Place.objects.filter(placeHolder=request.user.id)
        return render(request, 'cinemaApp/my_tickets.html', {'tickets': tickets})
    else:
        messages.success(
            request, ('You must be authorized to view "My Tickets" page.'))
        return redirect('login')


def show_session(request, session_id):
    if request.method == 'POST':
        booked_seats = request.POST['booked_seats']
        sitsEqualsZero = False
        # to catch case when string may not be converted to int using standart Python method
        try:
            int(booked_seats)
            sitsEqualsZero = True
        except Exception as e:
            pass
        if not sitsEqualsZero and booked_seats != '':
            sits = booked_seats.split(' | ')
            sitsIntegerList = list()
            for sit in sits:
                if sit != '':
                    sitsIntegerList.append(int(sit))
            for i in range(len(sitsIntegerList)):
                place = Place.objects.get(
                    session=session_id, placeNumber=sitsIntegerList[i])
                place.isAvaliable = False
                place.placeHolder = request.user.id
                place.save()
            messages.success(
                request, ('Tickets were successfully bought.'))
            return redirect('my-tickets')
        else:
            messages.success(
                request, ("You didn't chose any sit."))
            session = Session.objects.get(pk=session_id)
            seats = Place.objects.filter(session=session)
            return render(request, 'cinemaApp/show_session.html', {'session': session, 'seats': seats})
    else:
        session = Session.objects.get(pk=session_id)
        seats = Place.objects.filter(session=session)
        return render(request, 'cinemaApp/show_session.html', {'session': session, 'seats': seats})


def all_sessions(request):
    session_list = Session.objects.all().order_by('start_time')

    sessionFilter = SessionFilter(request.GET, queryset=session_list)
    session_list = sessionFilter.qs

    paginator = Paginator(session_list, 2)
    page = request.GET.get('page')
    sessions = paginator.get_page(page)

    return render(request, 'cinemaApp/sessions_list.html',
                  {'sessionList': session_list, 'filter': sessionFilter, 'sessions': sessions})


def home(request):
    return render(request, 'cinemaApp/home.html', {})


def load_halls(request):
    cinema_id = request.GET.get('cinema_id')
    halls = Hall.objects.filter(cinema_id=cinema_id)
    return render(request, 'cinemaApp/hall_dropdown_list_options.html', {'halls': halls})

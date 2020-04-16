from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from user.models import Student, Teacher, Staff, Adminn, Booking, Booking_student, Booking_teacher, Booking_staff, Booking_list, Room, Room_type

# Create your views here.
# @login_required(login_url='/')
# @permission_required('user.view_room', login_url='/')
def index(request):
    search_txt = request.POST.get('search','')
    all_room = Room.objects.filter(
        name__icontains= search_txt ).order_by('name')
    type = Room_type.objects.all()
    context = {
        'all_room': all_room,
        'type': type,   


    }


    return render(request, 'user/index.html', context)


def bookinglistall(request):

    return render(request, 'user/bookinglist.html')

def bookinglist(request):

    return render(request, 'user/bookinglistme.html')

def booking(request):

    return render(request, 'user/booking.html')

def profile(request):

    return render(request, 'user/profile.html')


def bookcheck(request):

    return render(request, 'user/bookcheck.html')

def add(request):
    context = dict()
    type = Room_type.objects.all()
    context['type'] = type

    if request.method == 'POST':
        name = request.POST.get('name')
        opentime = request.POST.get('st_time')
        closetime = request.POST.get('ed_time')
        capacity = request.POST.get('cap')
        type = request.POST.get('type')


        try:
            room = Room.objects.get(name=request.POST.get('name'))
        except ObjectDoesNotExist:
            room = None

        if room:
            context['error'] = 'ห้องซ้ำ'
            return render(request, 'user/addroom.html', context=context)     
        else:
            room = Room.objects.create(
            name = name,
            start_time = opentime,
            end_time = closetime,
            capacity = capacity

            )
            room.save()
            return redirect('index')
    
    return render(request, 'user/addroom.html', context=context)

def edit(request):

    return render(request, 'user/editroom.html')

def tracking(request):

    return render(request, 'user/track.html')
def accept(request):

    return render(request, 'user/accept.html')

def delete(request, rm_id):
    room = Room.objects.get(pk=rm_id)
    room.delete()
    return redirect('index')

def bookinglistadmin(request):

    return render(request, 'user/bookinglistadmin.html')

def history(request):

    return render(request, 'user/history.html')
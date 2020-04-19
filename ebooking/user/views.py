from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from user.models import Student, Teacher, Staff, Adminn, Booking, Booking_student, Booking_teacher, Booking_staff, Booking_list, Room, Room_type
from user.forms import EditForm, AddRoomForm
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
    all_booklist = Booking_list.objects.all()
    count = Booking_list.objects.count()
    context = {
        'all_booklist' : all_booklist,
        'count' : count,
    }
    return render(request, 'user/bookinglist.html', context)

def bookinglist(request):
    all_booklist = Booking_list.objects.all()
    user_id = request.user.id
    context = {
        'all_booklist' : all_booklist,
        'user_id' : user_id,
    }
    return render(request, 'user/bookinglistme.html', context)

def booking(request):

    return render(request, 'user/booking.html')

# def profile_edit(request):
#     context = {}
#     user = request.user
#     if request.method == 'POST':     

#         user.first_name = request.POST.get('fname')
#         user.last_name = request.POST.get('lname')
#         user.save()

#         return redirect('profile_edit')
#     return render(request, 'user/profile.html', context)

def profile(request):
    context = {}
    try:
        user_id = request.user.id
        student = Student.objects.get(user_id__exact=user_id)
        context['student'] = student
    except ObjectDoesNotExist:
        student = None
   
    
    if request.method == 'POST':
        username = request.user.username
        user = User.objects.get(username__exact=username)
        # oldpassword1 = request.user.password
        # oldpassword2 = request.POST.get('oldpass')
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')
        # check that the passwords match

        # matchcheck = check_password(oldpassword1, oldpassword2)
        # if matchcheck:
        if password1 == password2:
            user.set_password(password1)
            user.save()

            logout(request)
            return redirect('login')
        else:
                context['error'] = 'รหัสผ่านไม่ตรงกัน'
        # else:
        #         context['error'] = 'OldPasswords do not match.' 
         

    return render(request, 'user/profile.html', context)


def bookcheck(request, rm_id):
    room = Room.objects.get(pk=rm_id)
    all_booklist = Booking_list.objects.all()
    context = {
        'all_booklist' : all_booklist,
        'room' : room,


    }
    return render(request, 'user/bookcheck.html', context)

# def add(request):
#     context = dict()
#     type = Room_type.objects.all()
#     context['type'] = type

#     if request.method == 'POST':
#         name = request.POST.get('name')
#         opentime = request.POST.get('st_time')
#         closetime = request.POST.get('ed_time')
#         capacity = request.POST.get('cap')
#         roomType = request.POST.get('typeselect')


#         try:
#             room = Room.objects.get(name=request.POST.get('name'))
#         except ObjectDoesNotExist:
#             room = None

#         if room:
#             context['error'] = 'ห้องซ้ำ'
#             return render(request, 'user/addroom.html', context=context)     
#         else:
#             room = Room.objects.create(
#             name = name,
#             start_time = opentime,
#             end_time = closetime,
#             capacity = capacity,
#             room_type = Room_type.objects.get(pk=roomType)

#             )
#             room.save()
#             return redirect('index')
    
#     return render(request, 'user/addroom.html', context=context)


def add(request):
    context = dict()
    type = Room_type.objects.all()
    context['type'] = type

    if request.method == 'POST':
        form = AddRoomForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            capacity = request.POST.get('capacity')
            room_type = request.POST.get('room_type')


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
                start_time = start_time,
                end_time = end_time,
                capacity = capacity,
                room_type = Room_type.objects.get(pk=room_type)
                )
                room.save()
                return redirect('index')
        
    else:
        context['form'] = AddRoomForm()
    
    return render(request, 'user/addroom.html', context)


def edit(request, rm_id):
    room = Room.objects.get(pk=rm_id)
    type = Room_type.objects.all()
    if request.method == 'POST':     

        room.name = request.POST.get('name')
        room.open_time = request.POST.get('st_time')
        room.close_time = request.POST.get('ed_time')
        room.capacity = request.POST.get('cap')
        room.save()

        return redirect('index')
    context = {
        'room': room,
        'room_id' : rm_id,
        'type' : type 

        }

    return render(request, 'user/editroom.html', context)

def tracking(request, bl_id):
    book_list = Booking_list.objects.get(pk=bl_id)
    context = {
        'book_list': book_list,
    }
    return render(request, 'user/track.html', context)
def accept(request, bl_id):

    

    book_list = Booking_list.objects.get(pk=bl_id)
    context = {
        'book_list': book_list,
    }
  
    return render(request, 'user/accept.html', context)

def delete(request, rm_id):
    room = Room.objects.get(pk=rm_id)
    room.delete()
    return redirect('index')

def bookinglistadmin(request):
    all_booklist = Booking_list.objects.all()
    user_id = request.user.id
    context = {
        'all_booklist' : all_booklist,
        'user_id' : user_id
     
    }
    return render(request, 'user/bookinglistadmin.html', context)

def history(request):
   
    all_booklist = Booking_list.objects.all()
   
    context = {
        'all_booklist' : all_booklist,

     
    }
    return render(request, 'user/history.html', context)
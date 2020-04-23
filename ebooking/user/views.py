from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.db.models import Subquery
from user.models import Student, Teacher, Staff, Adminn, Booking, Booking_student, Booking_teacher, Booking_staff, Booking_list, Room, Room_type
from user.forms import EditForm, AddRoomForm, BookRoomForm
from django.forms import formset_factory
from user.forms import EditForm, AddRoomForm
from django.http import JsonResponse
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

# @csrf_exempt
# def api(request):
#     if request.method == 'GET':
#         room = Room.objects.all()
#         serializer = ToDoItemSerializer(room, many=True)
#         return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    # elif request.method == 'POST':
    #     serializer = ToDoItemSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def bookinglistall(request):
    all_booklist = Booking_list.objects.all()
    count = Booking_list.objects.count()
    context = {
        'all_booklist' : all_booklist,
        'count' : count,
    }
    return render(request, 'user/bookinglist.html', context)

def bookinglist(request): #existing booking list from users' requests
    all_booklist = Booking_list.objects.all()
    user_id = request.user.id
    context = {
        'all_booklist' : all_booklist,
        'user_id' : user_id,
    }
    return render(request, 'user/bookinglistme.html', context)

def booking(request): #func called by booking.html
    BookRoomFormSet = formset_factory(BookRoomForm)
    formset = BookRoomFormSet()
    data = {
            'formset-0-raw': 'my raw field string',
            'formset-INITIAL_FORMS': 1,
            'formset-TOTAL_FORMS': 2
            }
    # if request.method == 'POST':
        
    
    context = {}
    context['formset'] = formset
    context['data'] = data
    return render(request, 'user/booking.html', context)

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
        list = Booking.objects.filter(user_id=user_id).count()
        print(list)
        context['student'] = student
        context['list'] = list

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

    
    if request.method == 'POST':
        form = AddRoomForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            capacity = request.POST.get('capacity')
            room_type = request.POST.get('room_type')


            # try:
            #     room = Room.objects.get(name=request.POST.get('name'))
            # except ObjectDoesNotExist:
            #     room = None

            # if room:
            #     context['error'] = 'ห้องซ้ำ'
            #     context['form'] = AddRoomForm()
            #     # return render(request, 'user/addroom.html', context=context)     
            # else:
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
        form = AddRoomForm()
    return render(request, 'user/addroom.html', {'form': form})


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

    listno = Booking_list.objects.filter(list_no=bl_id).values_list('booking_id_id')
    booking = Booking.objects.filter(id__in = Subquery(listno)).values_list('id')
    booking_st = Booking_student.objects.filter(booking_id__in =  Subquery(booking))
 
    

    book_list = Booking_list.objects.get(pk=bl_id)
    print(booking_st)
    student = Student.objects.all()

    book_id = Booking.objects.filter()

    context = {
        'book_list': book_list,
        'student': student,
        'booking_st': booking_st,
    



    }
    return render(request, 'user/track.html', context)
def accept(request, bl_id):
    student = Student.objects.all()
    book_list = Booking_list.objects.get(pk=bl_id)
    context = {
        'book_list': book_list,
        'student': student,

    }
  
    return render(request, 'user/accept.html', context)

def delete(request, rm_id):
    room = Room.objects.get(pk=rm_id)
    room.delete()
    return redirect('index')

def track_delete(request, bl_id):
    listno = Booking_list.objects.filter(list_no=bl_id).values_list('booking_id_id')
    booking = Booking.objects.filter(id__in = Subquery(listno))
    booking.delete()
    return redirect('bookinglist')

def bookinglistadmin(request):
    all_booklist = Booking_list.objects.all()
    user_id = request.user.id
    context = {
        'all_booklist' : all_booklist,
        'user_id' : user_id
     
    }
    return render(request, 'user/bookinglistadmin.html', context)

def history(request):
    user = User.objects.all()
    st_booking = Booking_student.objects.all()
    all_booklist = Booking_list.objects.all()
   
    context = {
        'all_booklist' : all_booklist,
        'st_booking' : st_booking,
        'user' : user,



     
    }
    return render(request, 'user/history.html', context)
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.db.models import Subquery
from user.models import Student, Teacher, Staff, Adminn, Booking, Booking_student, Booking_teacher, Booking_staff, Booking_list, Room, Room_type, UserRole
from user.forms import EditForm, AddRoomForm, BookRoomForm
from django.forms import formset_factory
from user.forms import EditForm, AddRoomForm, BookRoomDescriptionForm
from django.http import JsonResponse
from datetime import datetime

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
    search_txt = request.POST.get('search','')

    # if request.POST.get('select') == 1:
    #     all_booklist.objects.filter(roon_id__name__icontains = 'L308')
    #     count = all_booklist.count()

    all_booklist = Booking_list.objects.filter(
        room_id__name__icontains= search_txt ).order_by('bookdate')
    count = all_booklist.count()
    stbooking = Booking_student.objects.all()
    context = {
        'all_booklist' : all_booklist,
        'count' : count,
        'stbooking' : stbooking,

    }
    return render(request, 'user/bookinglist.html', context)

def bookinglist(request): #existing booking list from users' requests

    all_booklist = Booking_list.objects.all().order_by('bookdate')
    user_id = request.user.id
    context = {
        'all_booklist' : all_booklist,
        'user_id' : user_id,
    }



    return render(request, 'user/bookinglistme.html', context)

def booking(request, rm_id): #func called by booking.html
    BookRoomFormSet = formset_factory(BookRoomForm)
    
    # data = {
    #         'formset-0-raw': 'my raw field string',
    #         'formset-INITIAL_FORMS': 1,
    #         'formset-TOTAL_FORMS': 2,
    #         }
    if request.method == 'POST':
        formset = BookRoomFormSet(request.POST)
        form = BookRoomDescriptionForm(request.POST)
        if formset.is_valid() and form.is_valid():
            
            booking = Booking.objects.create(
                description = form.cleaned_data['description'],
                user_id = request.user
            )
            booking.save()
            print('amount =', len(formset))
            print(formset)
            print('===================================================')
            for eachForm in formset:
                # print(eachForm.cleaned_data['start_time'])
                print(eachForm)
                booking_list = Booking_list.objects.create(                      
                    start_time = eachForm.cleaned_data['start_time'],
                    end_time = eachForm.cleaned_data['end_time'],
                    bookdate = eachForm.cleaned_data['bookdate'],
                    booking_id = booking,
                    room_id = Room.objects.get(id=rm_id)
                    
                    
                )
                
                
                booking_list.save()
                print(booking_list)
            return redirect('index')
            
            
    else:
        formset = BookRoomFormSet()
        form = BookRoomDescriptionForm()
        
        
    
    context = {}
    context['formset'] = formset
    # context['data'] = data
    context['form'] = form
    context['rm_id'] = rm_id
    return render(request, 'user/booking.html', context)



def profile(request):
    context = {}

    try:
        user_id = request.user.id
        role = UserRole.objects.get(user_id__exact=user_id)
        student = Student.objects.get(user_id__exact=user_id)
        list = Booking_list.objects.filter(booking_id__user_id=user_id).count()
        accept = Booking_list.objects.filter(booking_id__user_id=user_id, booking_id__status='2').count()
        user = request.user
        # print(myrole)
        context['student'] = student
        context['list'] = list
        context['accept'] = accept
        context['role'] = role


 


    except ObjectDoesNotExist:
        student = None
   
    
    if request.method == 'POST':
        if 'submitpass' in request.POST:
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
           
        elif 'submitname' in request.POST:
            user.first_name = request.POST.get('fname')
            user.last_name = request.POST.get('lname')
            user.save()
            context['success'] = 'แก้ไขข้อมูลสำเร็จ'
        

     
         

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
    context = {}
    allroom = Room.objects.all()
    room = Room.objects.get(pk=rm_id)
    type = Room_type.objects.all()
    

    if request.method == 'POST':     
        
        for all in allroom:
            if all.name == request.POST.get('name') and room.name != request.POST.get('name'):
                print('not equal')
                context['error'] = "ห้องซ้ำ"

        if room.name == request.POST.get('name'):
            print('equal')
            room.name = request.POST.get('name')
            room.start_time = request.POST.get('st_time')
            room.end_time = request.POST.get('ed_time')
            room.capacity = request.POST.get('cap')
            room.room_type_id = request.POST.get('type')
            room.save()

            return redirect('index')

        else:
            print('ไม่ซ้ำ')
            room.name = request.POST.get('name')
            room.start_time = request.POST.get('st_time')
            room.end_time = request.POST.get('ed_time')
            room.capacity = request.POST.get('cap')
            room.room_type_id = request.POST.get('type')
            room.save()
            return redirect('index')

    context['room'] = room
    context['room_id'] = rm_id
    context['type'] = type


    return render(request, 'user/editroom.html', context=context)



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
    book = Booking.objects.get(pk=book_list.booking_id.id)
  
    stu = Booking_student.objects.get(booking_id=book.id)
 
    context = {}
    context['book_list'] = book_list
    context['student'] = student
    context['bl_id'] = bl_id
    now = str(datetime.now())

    # t_result = False
    # s_result = False

    if request.method == 'POST':  

        if 'allowt' in request.POST:
            stu.teacher_result = True
            stu.teacher_date = now
            stu.save()
            t_result = True
        
            return redirect('bookinglistall')

        elif 'denyt' in request.POST:
            stu.teacher_result = False
            stu.save()
            t_result = False

            return redirect('bookinglistall')
        
        elif 'allows' in request.POST:
            stu.staff_result = True
            stu.staff_date = now
            stu.save()

            s_result = True
            return redirect('bookinglistall')

        elif 'denys' in request.POST:
            stu.staff_result = False
            stu.save()
            s_result = False


            return redirect('bookinglistall')
        
    # print("=================================2")
        
        
    # print('allow1')
    # print(stu.teacher_result)
    # print(stu.staff_result)
    # print(t_result)
    # print(s_result)


    # for st in studentbook:

    # if stu.teacher_result == True and stu.staff_result == True: 
        # book.status = '2'
        # book.save()

        # print('allow2')

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
    search_txt = request.POST.get('search','')
    all_booklist = Booking_list.objects.filter(
        room_id__name__icontains= search_txt ).order_by('bookdate')
    user_id = request.user.id
    context = {
        'all_booklist' : all_booklist,
        'user_id' : user_id
     
    }
    return render(request, 'user/bookinglistadmin.html', context)

def history(request):
    try:
        user = User.objects.all()
        st_booking = Booking_student.objects.all()

        search_txt = request.POST.get('search','')
        all_booklist = Booking_list.objects.filter(
            room_id__name__icontains= search_txt ).order_by('bookdate')
   
        
    
    except ObjectDoesNotExist:
        st_booking = None

    context = {
            'all_booklist' : all_booklist,
            'st_booking' : st_booking,
            'user' : user,
    }

    return render(request, 'user/history.html', context)


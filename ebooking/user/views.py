from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.db.models import Subquery
from user.models import Student, Teacher, Staff, Adminn, Booking, Booking_student, Booking_teacher, Booking_staff, Booking_list, Room, Room_type
from django.forms import formset_factory
from user.forms import EditForm, AddRoomForm, BookRoomDescriptionForm, RangeBookingForm, BookRoomForm
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework.response import Response
from user.serializers import RoomSerializer,RoomTypeSerializer

from datetime import date, timedelta

# Create your views here.
# @login_required(login_url='/')
# @permission_required('user.view_room', login_url='/')
def index(request):

    all_room = Room.objects.all()
    type = Room_type.objects.all()
    
    context = {
        'all_room': all_room,
        'type': type,   


    }

    return render(request, 'user/index.html', context)

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomTypeList(generics.ListCreateAPIView):
    queryset = Room_type.objects.all()
    serializer_class = RoomTypeSerializer
 
class RoomFilter(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def isEqual(self, room):
        return room['room_type'] == self.type
    

    def get(self, request, *args, **kwarg):
        try:
            self.type = int(request.GET.get('type'))

            if self.type:
                room = Room.objects.all()
                serializer = RoomSerializer(room, many=True)
                filter_data = filter(self.isEqual, serializer.data)
            return Response(filter_data)
        except Exception as e:
            return Response({
                "error" : str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

def bookinglistall(request):
    context = {}

    # if request.POST.get('select') == 1:
    #     all_booklist.objects.filter(roon_id__name__icontains = 'L308')
    #     count = all_booklist.count()
    
    search_txt = request.POST.get('search','')
    all_booklist = Booking_list.objects.filter(
        Q(room_id__name__icontains= search_txt) & ~Q(booking_id__status ='2') ).order_by('bookdate')
    count = all_booklist.count()
    stbooking = Booking_student.objects.all()
    user_id = request.user.id
    
    context['all_booklist'] = all_booklist
    context['count'] = count
    context['stbooking'] = stbooking

    if request.user.groups.filter(name ='student').exists():
       context['group'] = 'นักศึกษา'
    elif request.user.groups.filter(name ='teacher').exists():
       context['group'] = 'อาจารย์'
    elif request.user.groups.filter(name ='staff').exists():
       context['group'] = 'บุคลากร'
    elif request.user.groups.filter(name ='admin').exists():
       context['group'] = 'ผู้ดูแลระบบ'
    

    
    
    return render(request, 'user/bookinglist.html', context=context)

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
        if 'normalBooking' in request.POST:
            formset = BookRoomFormSet(request.POST)
            form = BookRoomDescriptionForm(request.POST)
            if formset.is_valid() and form.is_valid():
                
                booking = Booking.objects.create(
                    description = form.cleaned_data['description'],
                    user_id = request.user
                )
                booking.save()
                for eachForm in formset:
                    # print(eachForm.cleaned_data['start_time'])
                    booking_list = Booking_list.objects.create(                      
                        start_time = eachForm.cleaned_data['start_time'],
                        end_time = eachForm.cleaned_data['end_time'],
                        bookdate = eachForm.cleaned_data['bookdate'],
                        booking_id = booking,
                        room_id = Room.objects.get(id=rm_id)
                        
                        
                    )
                    
                    
                    booking_list.save()
                return redirect('index')
        elif 'rangeBooking' in request.POST:
            rangeBookingForm = RangeBookingForm(request.POST)
            if rangeBookingForm.is_valid():   
                fromDate = rangeBookingForm.cleaned_data['fromDate']   # start date
                toDate = rangeBookingForm.cleaned_data['toDate']  # end date

                fromTIme = rangeBookingForm.cleaned_data['fromTime']
                toTime = rangeBookingForm.cleaned_data['toTime']
                
                delta = toDate - fromDate       # as timedelta
                print(fromDate)
                print(toDate)
                print(delta)
                
                booking = Booking.objects.create(
                        description = rangeBookingForm.cleaned_data['description'],
                        user_id = request.user
                    )
                for i in range(delta.days + 1):
                    day = fromDate + timedelta(days=i)
                    print(day)
                    
                    booking.save()
                    booking_list = Booking_list.objects.create(                      
                        start_time = fromTIme,
                        end_time = toTime,
                        bookdate = day,
                        booking_id = booking,
                        room_id = Room.objects.get(id=rm_id)   
                    )               
                    booking_list.save()
                return redirect('index')
            
                
            
            
    else:
        formset = BookRoomFormSet()
        form = BookRoomDescriptionForm()
        rangeBookingForm = RangeBookingForm()
        
        
    formset = BookRoomFormSet()
    form = BookRoomDescriptionForm()
    rangeBookingForm = RangeBookingForm()
    context = {}
    context['formset'] = formset
    # context['data'] = data
    context['form'] = form
    context['rm_id'] = rm_id
    context['rangeBookingForm'] = rangeBookingForm
    return render(request, 'user/booking.html', context)





def profile(request):
    context = {}

    try:
      
        user_id = request.user.id
       
        student = Student.objects.get(user_id__exact=user_id)
        list = Booking_list.objects.filter(booking_id__user_id=user_id).count()
        accept = Booking_list.objects.filter(booking_id__user_id=user_id, booking_id__status='2').count()
        user = request.user
       
        context['student'] = student
        context['list'] = list
        context['accept'] = accept
      


    except ObjectDoesNotExist:
        student = None

    if request.user.groups.filter(name ='student').exists():
       context['group'] = 'นักศึกษา'
    elif request.user.groups.filter(name ='teacher').exists():
       context['group'] = 'อาจารย์'
    elif request.user.groups.filter(name ='staff').exists():
       context['group'] = 'บุคลากร'
    elif request.user.groups.filter(name ='admin').exists():
       context['group'] = 'ผู้ดูแลระบบ'
    
    if request.method == 'POST':
        if 'submitpass' in request.POST:
            username = request.user.id
            user = User.objects.get(id__exact=username)
            password1 = request.POST.get('pass1')
            password2 = request.POST.get('pass2')
         
            if password1 == password2:
                user.set_password(password1)
                user.save()

                logout(request)
                return redirect('my_login')
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

   

    try:
        user_id = request.user.id
        teacher = Teacher.objects.filter(user_id_id=user_id).values_list('id')
        staff = Staff.objects.filter(user_id_id=user_id).values_list('id')

    except ObjectDoesNotExist:
        teacher = None
        staff = None

    # print(teacher)
    # print(staff)

    t_result = ''
    s_result = ''

    if request.method == 'POST':  

        if 'allowt' in request.POST:
            stu.teacher_result = '2'
            stu.teacher_date = now
            stu.teacher_user_id_id = teacher
            
            stu.save()
            if stu.teacher_result == '2' and stu.staff_result == '2':
                book.status = '2'
                book.save()
                print('===============1==================')
        
            return redirect('bookinglistall')

        elif 'denyt' in request.POST:
            stu.teacher_result = '3'
            stu.teacher_user_id_id = teacher
            stu.save()
            if stu.teacher_result == '3':
                stu.staff_result = '3'
                stu.save()
                book.status = '3'
                book.save()
                print('================2=================')


            return redirect('bookinglistall')
        
        elif 'allows' in request.POST:
            stu.staff_result = '2'
            stu.staff_date = now
            stu.staff_user_id_id = staff
            stu.save()
            if stu.staff_result == '2' and stu.staff_result == '2':
                book.status = '2'
                book.save()
                print('===============3==================')
  
            return redirect('bookinglistall')

        elif 'denys' in request.POST:
            stu.staff_result = '3'
            stu.staff_user_id_id = staff

            stu.save()
            if stu.staff_result == '3':
                stu.teacher_result = '3'
                stu.save()
                book.status = '3'
                book.save()
                print('================4=================')


            return redirect('bookinglistall')
        

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
            Q(room_id__name__icontains= search_txt) & ~Q(booking_id__status ='1')).order_by('bookdate')
        teacher =Teacher.objects.all()
        staff =Staff.objects.all()

    
    
    except ObjectDoesNotExist:
        st_booking = None  
        teacher = None
        staff = None


    context = {
            'all_booklist' : all_booklist,
            'st_booking' : st_booking,
            'user' : user,
            'teacher' : teacher,
            'staff' : staff,

    }

    return render(request, 'user/history.html', context)

def history_teacher(request):
    try:
        user = User.objects.all()
        teacher_book = Booking_teacher.objects.all()

        search_txt = request.POST.get('search','')
        all_booklist = Booking_list.objects.filter(
            room_id__name__icontains= search_txt ).order_by('bookdate')
   
        
    
    except ObjectDoesNotExist:
        st_booking = None

    context = {
            'all_booklist' : all_booklist,
            'teacher_book' : teacher_book,
            'user' : user,
    }

    return render(request, 'user/historyteacher.html', context)


def history_staff(request):
  

    return render(request, 'user/historystaff.html')



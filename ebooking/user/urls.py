"""ebooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.models import User

urlpatterns = [
    path('', views.index, name='index'),
    path('bookinglistall/', views.bookinglistall, name='bookinglistall'),
    path('bookinglist/', views.bookinglist, name='bookinglist'),
    path('booking/<int:rm_id>/', views.booking, name='booking'),
    path('booking2/<int:rm_id>/', views.booking2, name='booking2'),

    path('profile/', views.profile, name='profile'),
    path('bookcheck/<int:rm_id>/', views.bookcheck, name='bookcheck'),
    path('add/', views.add, name='add'),
    path('edit/<int:rm_id>/', views.edit, name='edit'),
    path('tracking/<int:bl_id>/', views.tracking, name='tracking'),
    path('accept/<int:bl_id>/', views.accept, name='accept'),
    path('bookinglistadmin/', views.bookinglistadmin, name='bookinglistadmin'),
    path('history/', views.history, name='history'),
    path('history/teacher/', views.history_teacher, name='history_teacher'),
    path('history/staff/', views.history_staff, name='history_staff'),

    path('delete/<int:rm_id>/',views.delete, name='delete'),
    path('track_delete/<int:bl_id>/',views.track_delete, name='track_delete'),
    path('room/',views.RoomList.as_view(), name='room'),
    path('roomfilter/',views.RoomFilter.as_view(), name='room_filter'),
    path('roomtype/',views.RoomTypeList.as_view(), name='roomtype'),






    # path('profile/edit/',views.profile_edit, name='profile_edit'),
]

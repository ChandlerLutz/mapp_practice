from django.urls import path, re_path
from msgs import views

urlpatterns = [
    re_path(r'^new$', views.new_thread, name='new_thread'), 
    re_path(r'^(\d+)/$', views.view_thread, name='view_thread'),
    re_path(r'^(\d+)/add_msg$', views.add_msg, name='add_msg'), 
]

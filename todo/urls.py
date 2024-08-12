from django.urls import path 
from . import views

urlpatterns = [
    path('task/',views.task,name="task"),
    path('mark_as_done/<int:id>/', views.mark_as_done, name="mark_as_done"),
    path('mark_as_undone/<int:id>/',views.mark_as_undone, name='mark_as_undone'),
    path('add_task/',views.add_task,name='add_task'),
    path('edit/<int:id>/',views.edit_task,name='edit_task'),
    path('<int:id>/',views.delete_task,name='delete_task'),
    path('login',views.login,name="login")
    
]
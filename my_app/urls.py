from django.urls import path
from . import views



urlpatterns=[
    path('',views.index),
    path('project/<int:my_id>/',views.ProjectViewMore),
    path('project/<int:project_id>/task/<int:task_id>',views.TaskViewMore),
    path('accounts/sign_up/',views.sign_up,name="sign-up")

]
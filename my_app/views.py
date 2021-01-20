from django.shortcuts import render
from .models import Project,Task, User
from django.http import HttpResponse, JsonResponse
import json
import base64
from os import path
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
@login_required
def index(request):
  
  projects = Project.objects.all()
  for eachProject in projects:
      tasks=Task.objects.filter(project=eachProject)
      eachProject.projectUsers=[eachProject.owner]
      for eachTask in tasks:
          eachProject.projectUsers.append(eachTask.assignee) 
      if(eachProject.image):
          pass
      else:
          eachProject.image="static/img/noimage.png"
  dFiles={
        "project":projects
  }
  print("HEREEEEE")
  print(request.POST)

  if 'projectname' in request.POST:
      print("here")
      user=User.objects.get(username=request.POST.get('projectuser'))
      print(user)
      AddProjectObj=Project(name=request.POST.get('projectname'),description=request.POST.get('projectdescription'),duration = request.POST.get('projectduration'),image=request.FILES.get('projectimage'),owner=user)
      AddProjectObj.save()
      return HttpResponseRedirect("/")
  if 'DeleteProject' in request.POST:
            print('Delete')
            Project.objects.get(id=request.POST.get('DeleteProject')).delete()
            return HttpResponseRedirect("/")

  return render(request, 'index.html',dFiles)

@login_required
def ProjectViewMore(request,my_id):
    project = Project.objects.get(id=my_id)
    task=Task.objects.filter(project=project)
    url="/project/"+str(my_id)
    if(project.image):
        if(path.isfile(str(project.image))==False):
            image_64_decode = base64.decodestring(bytes(project.image_encoded,'utf-8'))
            image_result = open(str(project.image), 'wb') # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            image_result.close()
    else:
        project.image="static/img/noimage.png"
    
    print(request.POST)

    if 'taskname' in request.POST:
      print("here")
      AddTaskObj=Task(name=request.POST.get('taskname'),description=request.POST.get('taskdescription'),startdate = request.POST.get('taskstartdate'),enddate = request.POST.get('taskenddate'),project=project)
      AddTaskObj.save()
      return HttpResponseRedirect(url)
    if 'projectname' in request.POST:
        print("here")
        project.name=request.POST.get('projectname')
        project.description=request.POST.get('projectdescription')
        project.duration = request.POST.get('projectduration')
        project.image=request.FILES.get('projectimage')
        project.save()
        return HttpResponseRedirect(url)
    if 'DeleteTask' in request.POST:
        print('Delete')
        Task.objects.get(id=request.POST.get('DeleteTask')).delete()
        return HttpResponseRedirect(url)

    

    dFiles={
        "project":project,
        "task":task
    }
    return render(request, 'project.html',dFiles)


@login_required
def TaskViewMore(request,project_id,task_id):
    project = Project.objects.get(id=project_id)
    task=Task.objects.get(id=task_id)
    url="/project/"+str(project_id)+"/task/"+str(task_id)
    
    user=User.objects.all()
   
    print(request.POST)
    if 'taskassignee' in request.POST:
        taskassignee=User.objects.get(username=request.POST.get('taskassignee'))

        task.assignee=taskassignee
        task.save()
        return HttpResponseRedirect(url)
   
    if 'assignmentdescription' in request.POST:
        print("ERROR")

        assignmentdescription=request.POST.get('assignmentdescription')
        print("ERROR1")

        assignmentfile=request.FILES.get('submissionfile')
        print("ERROR2")
        task.assignmentDescription=assignmentdescription
        task.assignmentFile=assignmentfile
        print("ITS FINE")
        task.save()

        return HttpResponseRedirect(url)

    if 'taskname' in request.POST:
        print("here")
        task.name=request.POST.get('taskname')
        task.description=request.POST.get('taskdescription')
        task.startdate = request.POST.get('taskstartdate')
        task.enddate = request.POST.get('taskenddate')
        task.save()
        return HttpResponseRedirect(url)
    
    dFiles={
        "task":task,
        "user":user,
        "project_id":project_id
    }
    return render(request, 'task.html',dFiles)

def sign_up(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request,user)
            return render(request,'index.html')
    context['form']=form
    return render(request,'registration/sign_up.html',context)
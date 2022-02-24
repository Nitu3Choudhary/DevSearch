from django.shortcuts import render,redirect
from django.http import HttpResponse
from project.models import Project,Review,Tag
from .forms import ProjectForm,ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import searchProjects
from .utils import paginateProjects
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage



def projects(request):
    project_list, search_query = searchProjects(request)
    print(project_list)
    project_list, custom_range, paginator, page = paginateProjects(request,project_list,3)
    
                                                                  
    context = {'projects':project_list,
                'search_query':search_query,
                'custom_range':custom_range,
                'paginator':paginator,
                'page':page,
                }
    return render(request,'projects.html',context)

def project(request,pk):
         
    proj = None  
    proj = Project.objects.get(id=pk)
    all_reviewer = proj.reviewers
    review_form = ReviewForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.project = proj
            review.owner = request.user.profile
            review.save()

            proj.getVoteCount
                        
            messages.success(request,'Comment Added Successfully')
            return redirect('project:project',pk=proj.id)
        else:
            messages.error(request,'Error occurred')
        
        

            
    context = {'proj': proj,'review_form':review_form ,'all_reviewer':all_reviewer}

    return render(request, 'single-project.html', context)
    

@login_required(login_url='users:login')              
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile

            project.save()
            messages.success(request,'Project created successfully')
            return redirect('users:account')
        else:
            messages.error(request,'Some error occurred')    
    context = {'form':form}
    return render(request,'create-project.html',context)

@login_required(login_url='users:login')
def updateProject(request,pk):
    profile = request.user.profile

    p = Project.objects.get(id=pk) 
    form =ProjectForm(instance =p) 
    msg = ''


    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES, instance=p)
        if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('users:account')
        else:
            messages.error(request,'Some error occurred')    

    context = {'form':form,
                 'msg':msg,}
    return render(request,'update-project.html',context)


    

@login_required(login_url='users:login')
def deleteProject(request,pk):
    profile = request.user.profile
    p = Project.objects.get(id=pk) 
    

    if request.method == 'POST':

        p.delete()
        messages.success(request,'Project deleted successfully')
        return redirect('users:account')

    context = {'object':p,}
    return render(request,'delete-project.html',context)


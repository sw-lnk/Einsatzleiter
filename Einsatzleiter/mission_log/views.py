from django.shortcuts import HttpResponse, render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from .models import Mission
from .forms import NewMission

# Create your views here.

@login_required
def add(request):    
    # check if the request is post 
    if request.method =='POST':  
        
        # Pass the form data to the form class
        details = NewMission(request.POST)
 
        # In the 'form' class the clean function 
        # is defined, if all the data is correct 
        # as per the clean function, it returns true
        if details.is_valid():  
 
            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database   
            post = details.save(commit = False)
 
            # Finally write the changes into database
            post.save()  
    
            missions = Mission.objects.all()
            
            # redirect it to some another page indicating data
            # was inserted successfully
            return render(request, "mission_log/mission.html", {'mission_list':missions})
             
        else:
         
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "mission_log/mission_new.html", {'form':details})  
    else:
 
        # If the request is a GET request then,
        # create an empty form object and 
        # render it into the page
        form = NewMission(None)   
        return render(request, 'mission_log/mission_new.html', {'form':form})

@login_required
def all_missions(request):
    missions = Mission.objects.all()
    return render(request, "mission_log/mission.html", {'mission_list':missions})
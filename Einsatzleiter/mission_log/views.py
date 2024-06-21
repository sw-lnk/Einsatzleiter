import datetime

from django.shortcuts import HttpResponse, render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Mission
from .forms import NewMission, UpdateMission

# Create your views here.
def dashboard(request):
    context = {}
    
    context['cnt_untreaded'] = Mission.objects.filter(archiv=False, status=Mission.UNTREATED).count()
    context['cnt_processing'] = Mission.objects.filter(archiv=False, status=Mission.PROCESSING).count()
    context['cnt_closed'] = Mission.objects.filter(archiv=False, status=Mission.CLOSED).count()
    
    context['time_normal'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
    context['time_tactical'] = datetime.datetime.now().strftime('%d %H %M %b %y')
    
    return render(request, 'mission_log/dashboard.html', context)

@login_required
def all_missions(request):
    context = {}
    context['mission_list'] = Mission.objects.exclude(status__exact=Mission.CLOSED).order_by('prio', 'status', 'start',)
    context['mission_list_closed'] = Mission.objects.filter(status__exact=Mission.CLOSED).exclude(archiv__exact=True)
    return render(request, "mission_log/mission.html", context)

@login_required
def add(request):
    context = {}
    context['header'] = 'Neuer Einsatz'
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
            post.author = request.user
            # Finally write the changes into database
            post.save()
            
            # redirect it to some another page indicating data
            # was inserted successfully
            context['form'] = details
            context['header'] = 'Einsatz aktualisieren'
            return render(request, "mission_log/mission_create.html", context)
             
        else:
         
            # Redirect back to the same page if the data
            # was invalid
            context['form'] = details
            return render(request, "mission_log/mission_create.html", context)  
    else:
 
        # If the request is a GET request then,
        # create an empty form object and 
        # render it into the page
        context['form'] = NewMission(None)   
        return render(request, 'mission_log/mission_create.html', context)

@login_required
def update(request, main_id):
    context = {}
    context['header'] = 'Einsatz Aktualisieren'
    
    mission = get_object_or_404(Mission, main_id=main_id)
    form = UpdateMission(instance=mission)
    if request.method == "POST":
        form = UpdateMission(request.POST, instance=mission)
        if form.is_valid():
            form.save()
            context['form'] = form
            return render(request, "mission_log/mission_create.html", context)
    
    context['mission'] = mission
    context['form'] = form
    return render(request, 'mission_log/mission_create.html', context)

@login_required
def archiv_ask(request, main_id):    
    mission = get_object_or_404(Mission, main_id=main_id)
    return render(request, 'mission_log/mission_archiv.html', {'mission': mission})

@login_required
def archiv(request, main_id):    
    mission = get_object_or_404(Mission, main_id=main_id)
    mission.archiv = not mission.archiv
    mission.save()
    return redirect("mission_all")

import datetime

from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Mission, Entry, Vehicle
from .forms import NewMission, UpdateMission, NewEntry

def get_all_vehicles(mission:Mission=None, exclude_status_6=True) -> list[Vehicle]:
    all_vehicles = Vehicle.objects.exclude(status=2)
    
    if exclude_status_6:
        all_vehicles = all_vehicles.exclude(status=6)
    
    if mission:
        all_vehicles = all_vehicles.filter(mission=mission)
    
    return all_vehicles.order_by('call_sign')

def get_staff_dict(all_vehicles: list[Vehicle]) -> dict:
    return {
        'vf': sum([v.vf for v in all_vehicles]),
        'zf': sum([v.zf for v in all_vehicles]),
        'gf': sum([v.gf for v in all_vehicles]),
        'ms': sum([v.ms for v in all_vehicles]),
        'agt': sum([v.agt for v in all_vehicles]),
        'total': sum([v.staff_total() for v in all_vehicles])
    }

# Create your views here.
def dashboard(request):
    context = {}
    
    context['cnt_untreaded'] = Mission.objects.filter(archiv=False, status=Mission.UNTREATED).count()
    context['cnt_processing'] = Mission.objects.filter(archiv=False, status=Mission.PROCESSING).count()
    context['cnt_closed'] = Mission.objects.filter(archiv=False, status=Mission.CLOSED).count()
    
    context['time_normal'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
    context['time_tactical'] = datetime.datetime.now().strftime('%d %H %M %b %y')
    
    all_vehicles = get_all_vehicles()
    context['all_vehicles'] = all_vehicles
    context['staff'] = get_staff_dict(all_vehicles)
    
    return render(request, 'mission_log/dashboard.html', context)

@login_required
def all_missions(request):
    context = {}
    all_mission = Mission.objects.exclude(status__exact=Mission.CLOSED).order_by('prio', 'status', 'start',)
    missions = []
    for mission in all_mission:
        missions.append({
            'mission': mission,
            'vehicles': get_all_vehicles(mission),
            'staff': get_staff_dict(get_all_vehicles(mission))            
        })
    
    context['missions'] = missions
    
    #context['mission_list'] = Mission.objects.exclude(status__exact=Mission.CLOSED).order_by('prio', 'status', 'start',)
    context['mission_list_closed'] = Mission.objects.filter(status__exact=Mission.CLOSED).exclude(archiv__exact=True).order_by('-start')
    return render(request, "mission_log/mission.html", context)

@login_required
def add(request):
    context = {}
    context['header'] = 'Neuer Einsatz'
    
    # check if the request is post 
    if request.method =='POST':  
        
        # Pass the form data to the form class
        new_mission = NewMission(request.POST)
 
        # In the 'form' class the clean function 
        # is defined, if all the data is correct 
        # as per the clean function, it returns true
        if new_mission.is_valid():  
 
            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database   
            mission = new_mission.save(commit = False)
            mission.author = request.user
            # Finally write the changes into database
            mission.save()
            
            entry = Entry()
            entry.text = f"Einsatz erstellt: {mission.auto_entry()}"
            entry.author = request.user
            entry.mission = mission
            entry.save()
            
            # redirect it to some another page indicating data
            # was inserted successfully
            context['form'] = new_mission
            context['header'] = 'Einsatz aktualisieren'
            return redirect("mission_all", main_id=mission.main_id)
             
        else:
         
            # Redirect back to the same page if the data
            # was invalid
            context['form'] = new_mission
            return render(request, "mission_log/mission_detail.html", context)  
    else:
 
        # If the request is a GET request then,
        # create an empty form object and 
        # render it into the page
        context['form'] = NewMission(None)   
        return render(request, 'mission_log/mission_detail.html', context)

@login_required
def update(request, main_id):
    context = {}
    context['header'] = 'Einsatz Aktualisieren'
    context['form_entry'] = NewEntry(None)
    
    mission = get_object_or_404(Mission, main_id=main_id)
    form_mission = UpdateMission(instance=mission)
    if request.method == "POST":
        form_mission = UpdateMission(request.POST, instance=mission)
        if form_mission.is_valid():
            mission = form_mission.save()
            
            entry = Entry()
            entry.text = f"Einsatz aktualisiert: {mission.auto_entry()}"
            entry.author = request.user
            entry.mission = mission
            entry.save()
            
            context['form'] = form_mission
            return redirect("mission_all", main_id=mission.main_id)
    
    context['mission'] = mission
    context['form'] = form_mission    
    return render(request, 'mission_log/mission_detail.html', context)

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

@login_required
def mission_overview(request, main_id):    
    context = {}
    mission = get_object_or_404(Mission, main_id=main_id)
    context['mission'] = mission
    
    context['all_entries'] = Entry.objects.filter(mission=mission).order_by('-time')
    all_vehicles = get_all_vehicles()
    context['all_vehicles'] = all_vehicles
    context['staff'] = context['staff'] = get_staff_dict(all_vehicles)
    
    
    # check if the request is post 
    if request.method =='POST':  
        
        # Pass the form data to the form class
        new_entry = NewEntry(request.POST)
 
        # In the 'form' class the clean function 
        # is defined, if all the data is correct 
        # as per the clean function, it returns true
        if new_entry.is_valid():  
 
            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database   
            entry = new_entry.save(commit = False)
            entry.author = request.user
            entry.mission = mission
            # Finally write the changes into database
            entry.save()
            
            # redirect it to some another page indicating data
            # was inserted successfully
            context['all_entries'] = Entry.objects.filter(mission=mission).order_by('-time')
            return redirect("mission_all", main_id=mission.main_id)
             
        else:
         
            # Redirect back to the same page if the data
            # was invalid
            context['form'] = new_entry
            return render(request, "mission_log/mission_overview.html", context)  
    else:
 
        # If the request is a GET request then,
        # create an empty form object and 
        # render it into the page
        context['form'] = NewEntry(None)
    
    return render(request, 'mission_log/mission_overview.html', context)

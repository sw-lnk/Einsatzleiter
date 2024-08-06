import datetime
import io

from django.db.models import Case, When
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from .tables import MissionHTMxTable
from .filters import MissionFilter

from .models import Mission, Entry, Orga, Unit
from .forms import NewMission, UpdateMission, NewEntry, UpdateUnit

from .helper import get_all_units, get_staff_dict

from reports.mission_report import Report
from reports.unit_report import UnitOverview

# Create your views here.
def dashboard(request):
    context = {}
    
    context['cnt_untreaded'] = Mission.objects.filter(archiv=False, status=Mission.Status.UNTREATED).count()
    context['cnt_processing'] = Mission.objects.filter(archiv=False, status=Mission.Status.PROCESSING).count()
    context['cnt_closed'] = Mission.objects.filter(archiv=False, status=Mission.Status.CLOSED).count()
    
    context['time_normal'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
    context['time_tactical'] = datetime.datetime.now().strftime('%d %H %M %b %y')
    
    all_units = get_all_units(exclude_status_6=False)
    context['all_units'] = all_units
    context['staff'] = get_staff_dict(all_units)
    
    return render(request, 'mission_log/dashboard.html', context)

@login_required
def add(request):
    context = {}
    context['header'] = 'Neuer Einsatz'
    
    # check if the request is post 
    if request.method =='POST':  
        
        # Pass the form data to the form class
        new_mission = NewMission(request.POST)
        context['form'] = new_mission
 
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
            context['header'] = 'Einsatz aktualisieren'
            return redirect("mission_overview", main_id=mission.main_id)
             
        else:
         
            # Redirect back to the same page if the data
            # was invalid            
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
            new_mission_id = form_mission.cleaned_data['main_id']
            mission = form_mission.save()           
            
            entry = Entry()
            entry.text = f"Einsatz aktualisiert: {mission.auto_entry()}"
            entry.author = request.user
            entry.mission = mission
            entry.save()
            
            if main_id != new_mission_id:
                Entry.objects.filter(mission_id=main_id).update(mission_id=new_mission_id)
                Unit.objects.filter(mission_id=main_id).update(mission_id=new_mission_id)
                Mission.objects.get(main_id=main_id).delete()
            
            context['form'] = form_mission
            return redirect("mission_detail", main_id=mission.main_id)
    
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
    Unit.objects.filter(mission=mission).update(mission=None)
    return redirect("mission_all")

@login_required
def mission_overview(request, main_id):    
    context = {}
    mission = get_object_or_404(Mission, main_id=main_id)
    context['mission'] = mission
    
    context['all_entries'] = Entry.objects.filter(mission=mission).order_by('-time')
    all_units = get_all_units(mission=mission)
    context['all_units'] = all_units
    context['staff'] = get_staff_dict(all_units)
    
    
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
            return redirect("mission_overview", main_id=mission.main_id)
             
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

@login_required
def download_mission_report(request, main_id):
    mission = Mission.objects.get(main_id=main_id)
    entries = Entry.objects.filter(mission=mission).order_by('-time')
    units = Unit.objects.filter(mission=mission).order_by('call_sign')

    pdf = Report(request.user, mission, entries, units)
    output = pdf.output()
    buffer = io.BytesIO(output)
    
    file_name = f'{mission.keyword}-{mission.address()}.pdf'.replace(' ', '_').replace(',', '_')
    
    return FileResponse(
    buffer, as_attachment=False, # or False, depending upon the desired behavior
    filename=file_name, content_type='application/pdf'
    )

@login_required
def download_unit_report_incl2(request):
    units = Unit.objects.all().order_by('call_sign')

    pdf = UnitOverview(request.user, units)
    output = pdf.output()
    buffer = io.BytesIO(output)
    
    file_name = f"Kraefteuebersicht_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    
    return FileResponse(
    buffer, as_attachment=False, # or False, depending upon the desired behavior
    filename=file_name, content_type='application/pdf'
    )

@login_required
def download_unit_report_excl2(request):
    units = Unit.objects.all().exclude(status=2).order_by('call_sign')

    pdf = UnitOverview(request.user, units)
    output = pdf.output()
    buffer = io.BytesIO(output)
    
    file_name = f"Kraefteuebersicht_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    
    return FileResponse(
    buffer, as_attachment=False, # or False, depending upon the desired behavior
    filename=file_name, content_type='application/pdf'
    )

@login_required
def all_units(request):
    context = {}
    
    context['staff'] = get_staff_dict(get_all_units(exclude_status_6=False))
    
    all_orgas = Orga.objects.all()
    orgas = []
    order = Unit.STATUS_ORDER
    
    preferred = Case(
        *(
            When(status=id, then=pos)
            for pos, id in enumerate(order, start=1)
        )
    )
    
    for orga in all_orgas:        
        units = Unit.objects.filter(orga=orga).order_by(preferred, 'call_sign')
        
        orgas.append({
            'orga': orga,
            'units': units
            })
        
    context['orgas'] = orgas
    
    return render(request, "mission_log/unit_all.html", context)

@login_required
def unit_update(request, pk):
    context = {}
    context['header'] = 'Einheit Aktualisieren'
    
    unit = get_object_or_404(Unit, id=pk)
    context['unit'] = unit
    
    form_unit = UpdateUnit(instance=unit)
    form_unit.fields["mission"].queryset = Mission.objects.exclude(status=2)
    context['form'] = form_unit
    
    if request.method == "POST":        
        form_unit = UpdateUnit(request.POST, instance=unit)
        form_unit.fields["mission"].queryset = Mission.objects.exclude(status=2)
        context['form'] = form_unit
        if form_unit.is_valid():
            unit = form_unit.save()
            return redirect("unit_detail", pk=unit.id)
        else:
            return render(request, "mission_log/unit_detail.html", context)
    
    return render(request, 'mission_log/unit_detail.html', context)

@login_required
def unit_add(request):
    context = {}
    context['header'] = 'Einheit Anlegen'
    
    if request.method == "POST":        
        form_unit = UpdateUnit(request.POST)
        if form_unit.is_valid():
            unit = form_unit.save()
            return redirect("unit_detail", pk=unit.id)
        else:
            return render(request, "mission_log/unit_detail.html", context)
    
    form = UpdateUnit(None)
    form.fields["mission"].queryset = Mission.objects.exclude(status=2)
    context['form'] = form
    return render(request, 'mission_log/unit_detail.html', context)


# @login_required
class MissionHTMxTableView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = MissionHTMxTable
    queryset = Mission.objects.exclude(archiv=True).order_by('-start')
    filterset_class = MissionFilter
    paginate_by = 15

    def get_template_names(self):
        if self.request.htmx:
            template_name = "mission_log/mission_table_partial.html"
        else:
            template_name = "mission_log/mission_table_htmx.html"

        return template_name
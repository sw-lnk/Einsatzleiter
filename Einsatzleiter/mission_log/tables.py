import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from .models import Mission, Unit
from .helper import get_staff_dict

class MissionHTMxTable(tables.Table):
    main_id = tables.Column(attrs={"td": {"class": 'text-end'}})
    keyword = tables.Column(attrs={"td": {"class": 'text-start'}})
    
    staff = tables.Column(_('Staff'), empty_values=(), attrs={"td": {"class": 'text-end'}})
    
    address = tables.TemplateColumn(verbose_name=_('Address'),
        template_code='<a href="{% url "mission_overview" record.main_id %}" class="link-primary link-underline-opacity-0">{{ record.address }}</a>',
        order_by=('street', 'street_no', 'zip_code'),
        attrs={"td": {"class": 'text-start'}}
    )
    
    btn = tables.TemplateColumn(verbose_name='',
        template_name='mission_log/mission_table_btn.html'
    )
    
    prio = tables.TemplateColumn(verbose_name=_('Prio'),
        template_name='mission_log/mission_table_prio.html'
    )
    
    status = tables.TemplateColumn(
        template_name='mission_log/mission_table_status.html'
    )
    
    class Meta:
        model = Mission
        template_name = "tables/bootstrap_htmx.html"
        fields = ("main_id", "keyword", "address", "prio", "status", "staff", "start", 'btn')
        row_attrs = {
            'style': "white-space: nowrap;",
        }
        
    def render_staff(self, record):
        all_units = Unit.objects.filter(mission=record.main_id)
        staff = get_staff_dict(all_units)
        return f"{staff['vf']}/{staff['zf']}/{staff['gf']}/{staff['ms']} = {staff['total']}"
    
    
    
    
        
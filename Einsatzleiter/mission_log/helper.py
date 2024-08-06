from .models import Mission, Unit

def get_all_units(mission:Mission=None, exclude_status_6=True) -> list[Unit]:
    all_units = Unit.objects.exclude(status=2)
    
    if exclude_status_6:
        all_units = all_units.exclude(status=6)
    
    if mission:
        all_units = all_units.filter(mission=mission)
    
    return all_units.order_by('call_sign')

def get_staff_dict(all_units: list[Unit]) -> dict:
    return {
        'vf': sum([v.vf for v in all_units]),
        'zf': sum([v.zf for v in all_units]),
        'gf': sum([v.gf for v in all_units]),
        'ms': sum([v.ms for v in all_units]),
        'agt': sum([v.agt for v in all_units]),
        'total': sum([v.staff_total() for v in all_units])
    }
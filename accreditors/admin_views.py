from django.shortcuts import render
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from .models import Accreditor





@staff_member_required
def accreditor_application_count(request):
    accreditors = Accreditor.objects.annotate(application_count=Count('applications'))

    less_than_4 = []
    greater_or_equal_4 = []

    for accreditor in accreditors:
        if accreditor.application_count < 4:
            less_than_4.append(accreditor)
        else:
            greater_or_equal_4.append(accreditor)

    context = {
        'less_than_4': less_than_4,
        'greater_or_equal_4': greater_or_equal_4,
    }

    return render(request, 'admin/accreditor_list.html', context)

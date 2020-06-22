from django.shortcuts import render
from django.http import HttpResponseNotFound

from database.models import Asset


def all_assets(request):
        if request.user.is_superuser:
            if request.POST:
                pass
            context={
                'assets' : Asset.objects.all()
            }
            return render(request,'inventory/all_assets.html', context=context)
        return HttpResponseNotFound()
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .ic import calculate_results
from InvestClass import settings
import base64


# Create your views here.

def index(request):
    return render(request, 'index.html', {})


def ic(request):
    if request.method == 'POST':
        res = {}
        rc = request.POST.get('rc', default="0.25")
        cc = request.POST.get('cc', default="10000")
        l = request.POST.get('l', default="12")
        g = request.POST.get('g', default="0.1")
        b = request.POST.get('b', default="1")
        y = request.POST.get('y', default="0.05")
        print(rc, cc, l, g, b, y)
        res = calculate_results(float(rc), int(cc), int(l), float(g), float(b), float(y))
        Contributions = res['Contributions']
        Distributions = res['Distributions']
        NAV = res['NAV']
        IRR = res['IRR']
        img_path = settings.MEDIA_ROOT + '/ic.jpg'

        image_path = os.path.join(settings.MEDIA_ROOT, 'ic.jpg')

        # with open('/home/shuangkangde/InvestClass/media/ic.jpg', 'rb') as f:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        return render(request, 'ic.html', locals())

    return render(request, 'ic.html', {})

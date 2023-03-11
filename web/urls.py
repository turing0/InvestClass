from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ic', views.ic, name='ic'),
    # path('api/calc/', views.calc, name='calc'),
    # path('api/uwb/', views.uwb, name='uwb'),
    # path('api/trade/', views.trade, name='trade'),
    # path('api/balance/', views.balance, name='balance'),
    # path('api/getpos/', views.getpos, name='getpos'),
    # path('api/setpos/', views.setpos, name='setpos'),
    # path('api/pos/', views.pos, name='pos'),  # update position
    # path('show/', views.show, name='show'),
    # path('position/', views.position, name='position'),
]



from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('resolve-address-test', views.resolve_address,
         name="resolve_address-test"),
    path('resolve-address', views.ResolveAddress.as_view(), name="resolve_address"),
    path('deliveries', views.BookDelivery.as_view(), name="deliveries"),
    path('deliveries/daily', views.GetDailyDeliveries.as_view(),
         name="deliveries-daily"),
    path('deliveries/weekly', views.GetWeeklyDeliveries.as_view(),
         name="deliveries-weekly"),
    path('deliveries/<int:pk>/complete', views.CompleteDelivery.as_view()),
    path('deliveries/<int:pk>', views.CancelDelivery.as_view()),
    path('timeslots', views.GetTimeslotsForAddress.as_view())
]

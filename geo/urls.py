from django.urls import path
from geo import views


urlpatterns = [
    path('geo/api/<str:ip>/', views.IpDetails.as_view()), # Send single ip to api
    path('geo/api/filter/<str:filter>/', views.AllIpFilter.as_view()), # send city/country as filter to api
    path('geo/api/sort/<str:sort_flag>/', views.AllIpSort.as_view()), # view and sort all cached data by 'city' or 'country'
    path('', views.ListIPs.as_view()), # View ips and info in no particular order
]

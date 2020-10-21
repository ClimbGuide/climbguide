"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from users import views as user_views
from climbguide import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    # user URLS
    path('accounts/profile/', user_views.profile, name="profile"),
    # climbguide URLS
    path('', views.home, name='home'),
    path('search/', views.search, name="search"),
        # routes
    path('routes/detail/<int:route_pk>', views.route_detail, name="route_detail"),
    path('routes/detail/<int:route_pk>/addphoto/', views.addphoto_to_route, name="addphoto_to_route"),
        # daytrip
    path('daytrips/add/', views.add_daytrip, name="add_daytrip"),
    path('daytrips/detail/<int:daytrip_pk>', views.daytrip_detail, name="daytrip_detail"),
    path('daytrips/edit/<int:daytrip_pk>', views.edit_daytrip, name="edit_daytrip"),
    path('daytrips/delete/<int:daytrip_pk>', views.delete_daytrip, name="delete_daytrip"),
    path('daytrips/detail/<int:daytrip_pk>/addroute/<int:route_pk>', views.addroute_to_daytrip, name="addroute_to_daytrip"),

        # pointofinterest
    path('pointsofinterest/add/', views.add_pointofinterest, name="add_pointofinterest"),
    path('pointsofinterest/detail/<int:pointofinterest_pk>', views.pointofinterest_detail, name="pointofinterest_detail"),
    path('pointsofinterest/edit/<int:pointofinterest_pk>', views.edit_pointofinterest, name="edit_pointofinterest"),
    path('pointsofinterest/delete/<int:pointofinterest_pk>', views.delete_pointofinterest, name="delete_pointofinterest"),
    path('pointsofinterest/detail/<int:pointofinterest_pk>/addphoto/', views.addphoto_to_pointofinterest, name="addphoto_to_pointofinterest"),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

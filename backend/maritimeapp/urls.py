from django.urls import include, path

# from . import views
from .views import (download_data, get_display_info, list_sites,
                    set_csrf_token, site_measurements)

urlpatterns = [
    path("download/", download_data, name="download_data"),
    path("measurements/sites/", list_sites, name="list_sites"),
    path("measurements/", site_measurements, name="site_measurements"),
    path("display_info/", get_display_info, name="display_info"),
    path("set-csrf/", set_csrf_token, name="set-csrf"),
]

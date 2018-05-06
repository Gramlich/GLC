"""GLC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from accounts import views as accounts_views
from DataPresenter import views

urlpatterns = [
    path('', views.home_redirect, name='home_redirect'),
    path('home/', views.home, name='home'),
    path('data/', views.data, name='data'),
    path('signup', accounts_views.signup, name='signup'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('<slug>', views.graph, name='workout_graph'),
    path('graph/split_elp/<slug>', views.json_data_split_elp, name='json_data_split_elp'),
    path('graph/SR_DfS/<slug>', views.json_data_SR_DfS, name='json_data_SR_DfS'),
    path('graph/dps_elp/<slug>', views.json_data_dps_elp, name='json_data_dps_elp'),
    path('graph/dps_dfs/<slug>', views.json_data_dps_dfs, name='json_data_dps_dfs'),

    path('admin/', admin.site.urls),
]

# path('graph/', views.graph, name='graph'),

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

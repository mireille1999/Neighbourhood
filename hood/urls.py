from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static  import static


urlpatterns = [
    path('',views.index,name='index'),  
    path('hood/<location>',views.single_hood,name='single_hood'),
    path('profile/', views.profile, name='profile'),
    path('registration_form/',views.signup,name='signup'),
    path("login/", views.login_request, name="login_link"),
    path("logout", views.logout_request, name= "logout"),
    path("authorities/", views.authorities, name="authorities"),
    path("health/", views.health, name="health"),
]
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
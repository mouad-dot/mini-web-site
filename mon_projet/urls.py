from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('welcome/', views.welcome, name='welcome'),
    path('', include('login.urls')),
    # Commenter ou supprimer cette ligne si la vue 'lhegra' n'existe pas
    # path('zid/', views.lhegra, name='lhegra'),
    
    path('register/', views.register, name='register'),
    path('bienvenue/', views.bienvenue, name='bienvenue'),
    path('logout/', views.logout, name='logout'),
    path('modifier-profil/', views.modifier_profil, name='modifier_profil'),
    path('voir-profil/', views.voir_profil, name='voir_profil'),

    
]
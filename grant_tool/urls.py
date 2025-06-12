from django.contrib import admin
from django.urls import path, include
from grant_writer_app.views import grant_writer_ui 




urlpatterns = [
    path('admin/', admin.site.urls),
    path('grant_writer/', include('grant_writer_app.urls')),  
    path('', grant_writer_ui, name='home'), 
]

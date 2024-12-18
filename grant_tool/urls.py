from django.contrib import admin
from django.urls import path, include
from grant_writer_app.views import grant_proposal_form  # Import your view here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grant_writer/', include('grant_writer_app.urls')),  # Routes to app urls
    path('', grant_proposal_form, name='home'),  # Root path now routes to a view
]

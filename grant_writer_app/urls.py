from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.grant_proposal_form, name='grant_proposal_form'),
    path('generate/', views.generate_response, name='generate_response'),
    path('ui/', views.grant_writer_ui, name='grant_writer_ui'),  # New UI route
]

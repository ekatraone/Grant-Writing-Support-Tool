from django.contrib import admin
from django.urls import path
from app.views import analyze_text, index, analyze_page, privacy_policy, resources,transcribe_voice_note
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin path
    path('admin/', admin.site.urls),

    # App-specific URLs
    path('', index, name='index'),                # Home page
    path('analyze/', analyze_text, name='analyze_text'),  # Sentiment analysis page
    path('analyze-page/', analyze_page, name='analyze_page'),  # Analyze page
    path('privacy-policy/', privacy_policy, name='privacy_policy'),  # Privacy Policy page
    path('resources/', resources, name='resources'),  # Resources page
    path('transcribe-voice/', transcribe_voice_note, name='transcribe_voice'),

    # JWT Authentication URLs (for token generation and refreshing)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

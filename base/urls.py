from django.urls import path
from .views import SectionAPIView, AudioLatinAPIView, AudioCyrillicAPIView

urlpatterns = [
    path('sections', SectionAPIView.as_view()),
    path('section/<int:pk>/latin-audios', AudioLatinAPIView.as_view()),
    path('section/<int:pk>/cyrillic-audios', AudioCyrillicAPIView.as_view()),
]


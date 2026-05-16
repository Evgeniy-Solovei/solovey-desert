from django.urls import path

from . import api

app_name = 'pages_api'

urlpatterns = [
    path('hero-slides/', api.HeroSlideListAPIView.as_view(), name='hero_slide_list'),
]

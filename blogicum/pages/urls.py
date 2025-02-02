from django.urls import path
from .views import AboutView, RulesView  # Импортируем наши новые классы представлений

app_name ='pages'

urlpatterns = [
    # другие маршруты...
    path('about/', AboutView.as_view(), name='about'),
    path('rules/', RulesView.as_view(), name='rules'),
]
from django.urls import path
from .views import RegisterUser, LoginUser, SuggestPlant, SensorDataView

urlpatterns = [
    path('signup/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('suggest/', SuggestPlant.as_view()),        # old route
    path('suggest-plant/', SuggestPlant.as_view()),  # new route
    path('sensor/', SensorDataView.as_view()),       # sensor data API
]



from django.urls import path
from .views import QuizTake

app_name='quizz'
urlpatterns=[
    #quiz/3/
    path('<int:tutorial_id>/',view=QuizTake.as_view(),name='quiz_question'),
]
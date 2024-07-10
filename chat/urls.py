from django.urls import path
from .views import chat_view, chat_history

urlpatterns = [
    path("", chat_view, name="chat"),
    path("history/<str:chat_name>/", chat_history, name="chat_history"),
]

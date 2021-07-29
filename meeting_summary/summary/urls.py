from django.urls import path

from .views import (
    create_meeting_view
)


app_name = "summary"
urlpatterns = [
    path("summary/", view=create_meeting_view, name="summary"),
]

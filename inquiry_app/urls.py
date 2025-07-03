from django.urls import path
from . import views

urlpatterns = [
    path("", views.inquiry_form_view, name="inquiry_form"),
    path("records/", views.show_records_view, name="show_records"),
]

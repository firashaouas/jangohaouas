from django.urls import path
from . import views
from .views import *
urlpatterns =[
 #path("liste/", views.list_conferences, name="liste_conferences"),
    path("liste/",ConferenceList.as_view(),name="liste_conferences"),
    path("<int:pk>/",ConferenceDetails.as_view(),name="conference_details"),
    path("add/",ConferenceCreate.as_view(),name="conference_add"),
    path("edit/<int:pk>/",ConferenceUpdate.as_view(),name="conference_update"),
     path("delete/<int:pk>/",ConferenceDelete.as_view(),name="conference_delete"),
     path("submissions/add/", AddSubmission.as_view(), name="submission_add"),
path(
    "submissions/update/<str:pk>/",
    UpdateSubmission.as_view(),
    name="submission_update"
),

    # ✅ APRES : l’URL de détails
    path("submissions/<str:pk>/", DetailSubmission.as_view(), name="submission_details"),


     

]
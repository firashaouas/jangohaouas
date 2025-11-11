from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView , DetailView , CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import ConferenceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Submission
from django.http import HttpResponseForbidden

# Create your views here.


def list_conferences(request):
    conferences_list=Conference.objects.all()
    """retour : liste + page """
    return render(request,"conferences/liste.html", {"liste":conferences_list})

class ConferenceList(ListView):
    model=Conference
    context_object_name="liste"
    template_name="conferences/liste.html"

class ConferenceDetails(DetailView):
    model=Conference
    context_object_name="conference"
    template_name="conferences/details.html"

class ConferenceCreate(LoginRequiredMixin,CreateView):
    model= Conference
    template_name ="conferences/form.html"
    #fields = "__all__"
    form_class =ConferenceForm
    success_url = reverse_lazy("liste_conferences")

class ConferenceUpdate(LoginRequiredMixin,UpdateView):
    model =Conference
    template_name="conferences/form.html"
    #fields="__all__"
    form_class =ConferenceForm
    success_url=reverse_lazy("liste_conferences")

class ConferenceDelete(LoginRequiredMixin,DeleteView):
    model=Conference
    template_name ="conferences/conference_confirm_delete.html"
    success_url =reverse_lazy("liste_conferences")


from django.views.generic import ListView
from .models import Submission
from django.contrib.auth.mixins import LoginRequiredMixin

class SubmissionList(LoginRequiredMixin, ListView):
    model = Submission
    template_name = "submissions/liste.html"
    context_object_name = "submissions"

    def get_queryset(self):
        # Afficher seulement les soumissions de l'utilisateur connecté
        return Submission.objects.filter(user=self.request.user)

from django.views.generic import DetailView
from .models import Submission
from django.contrib.auth.mixins import LoginRequiredMixin

class DetailSubmission(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = "submissions/details.html"
    context_object_name = "submission"

from UserApp.models import User   # selon ton app

class AddSubmission(LoginRequiredMixin, CreateView):
    model = Submission
    template_name = "submissions/add.html"
    fields = ["title", "abstract", "keywords", "paper", "conference"]
    success_url = reverse_lazy("submission_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user   # ✅ l'utilisateur connecté
        form.instance.status = "submitted"
        return super().form_valid(form)

class UpdateSubmission(LoginRequiredMixin, UpdateView):
    model = Submission
    template_name = "submissions/update.html"
    fields = ["title", "abstract", "keywords", "paper"]
    success_url = reverse_lazy("submission_list")

    def dispatch(self, request, *args, **kwargs):
        submission = self.get_object()

        # 🔒 Vérification : seul le propriétaire peut modifier
        if submission.user != request.user:
            return HttpResponseForbidden("Tu n'as pas le droit de modifier cette soumission.")

        # 🔒 Vérification : statut accepté ou rejeté = modification interdite
        if submission.status in ["accepted", "rejected"]:
            return HttpResponseForbidden("Cette soumission ne peut plus être modifiée.")

        return super().dispatch(request, *args, **kwargs)
from django.db import models
from ConferenceApp.models import Conference
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Validator pour le nom de salle
name_validator = RegexValidator(
    regex=r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s]+$',
    message="Le nom de la salle ne peut contenir que lettres et chiffres (pas de caractères spéciaux)"
)

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=255, validators=[name_validator])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="sessions")

    def clean(self):
        # Vérifie que la conférence est sélectionnée
        if not self.conference_id:  # conference_id existe même si conference n'est pas chargé
            return  # On ne fait rien si pas encore de conférence

        # Vérifie que session_day est dans la plage de la conférence
        if self.session_day:
            start = self.conference.start_date
            end = self.conference.end_date
            if start and end and not (start <= self.session_day <= end):
                raise ValidationError(
                    "La date de la session doit être entre start_date et end_date de la conférence"
                )

        # Vérifie que start_time < end_time
        if self.start_time and self.end_time:
            if self.start_time> self.end_time:
                raise ValidationError("La date de début doit être inférieure à la date de fin")

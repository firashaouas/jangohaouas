from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError as validationError
from django.core.validators import RegexValidator 
from django.core.validators import FileExtensionValidator
from django.utils import timezone  
import uuid
name_validator = RegexValidator(
    regex=r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$',
    message="le titre de la conférence doit contenir uniquement des lettres et espaces"
)
def generate_sub_id():
   return "SUB-"+uuid.uuid4().hex[:8].upper()
file_validator=FileExtensionValidator(
   allowed_extensions=['pdf'],
   message="doit etre .pdf"
)
def maxi(keywords):
    s=[]
    for k in keywords.strip().split():
        if k!=' ':
            s.append(k)
    if len(s) > 10 :
        raise validationError("Maximum 10 mots-cles autorises")


class Conference(models.Model):
   Conference_id=models.AutoField(primary_key=True)
   name=models.CharField(max_length=255,validators=[name_validator])
   THEME=[
      ("IA","computer science & ia"),
      ("SE","Science & eng"),
      ("Sc","Social sciences"),
   ]
   theme=models.CharField(max_length=255,choices=THEME)
   location=models.CharField(max_length=255 )
   description=models.TextField(validators=[MaxLengthValidator(30,"attention")])
   start_date=models.DateField()
   end_date=models.DateField()
   created_at=models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   def __str__(self):
       return f'la conference a comme titre {self.name}'
       
   def clean(self):
     if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise validationError("La date de début doit être inférieure à la date de fin")
class Submission(models.Model):
    submission_id = models.CharField(max_length=255, primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.TextField(validators=[maxi])
    paper = models.FileField(upload_to="papers/", validators=[file_validator])
    STATUS = [
        ("submitted", "submitted"),
        ("under review", "under review"),
        ("rejected", "rejected"),
    ]
    status = models.CharField(max_length=50, choices=STATUS, default="submitted")
    payed = models.BooleanField(default=False)
    submission_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE, related_name="submissions")
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="submissions")

    def clean(self):
        today = timezone.now().date()

        if self.user and self.conference:
            submissions_today = Submission.objects.filter(
                user=self.user,
                submission_date__date=today
            ).count()

            if self.pk is None and submissions_today >= 3:
                raise validationError("Maximum 3 soumissions par jour")

            if today > self.conference.start_date:
                raise validationError("La soumission ne peut être faite que pour des conférences à venir")

    def save(self, *args, **kwargs):
        if not self.submission_id:
            newid = generate_sub_id()
            while Submission.objects.filter(submission_id=newid).exists():
                newid = generate_sub_id()
            self.submission_id = newid
        super().save(*args, **kwargs)
class OrganizinCommitte(models.Model):
   COMMITTE=[
      ("chair","chair"),
      ("co-chair","co-chair"),
      ("member","member"),
   ]
   committe_role=models.CharField(max_length=255,choices=COMMITTE,default="member")
   date_joined=models.DateField()
   created_at=models.DateTimeField(auto_now_add=True)
   update_at=models.DateTimeField(auto_now=True)
   user=models.ForeignKey("UserApp.User",on_delete=models.CASCADE,related_name="committees")
   conference=models.ForeignKey(Conference,on_delete=models.CASCADE,related_name="committess")
   
# Create your models here.
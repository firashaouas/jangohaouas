from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.exceptions import ValidationError as validationError
from django.core.validators import RegexValidator 
# Create your models here.
def generate_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()
def verifyemail(email):
    domaine=["esprit.tn","seasame.com","tek.tn"]
    email_domaine=email.split("@")[1]
    if not email_domaine in domaine:
        raise validationError("email domaine not allowed")  
name_validator=RegexValidator(
    regex=r'[a-zA-Z\s-]+$',
    message="les noms et prénoms ne doivent contenir que des lettres (et éventuellement des espaces ou tirets) "

)
class User(AbstractUser):
    user_id = models.CharField(max_length=8, primary_key=True, unique=True)
    first_name = models.CharField(max_length=255,validators=[name_validator])
    last_name = models.CharField(max_length=255,validators=[name_validator])
    ROLE = [
        ("IA", "computer science & ia"),
        ("SE", "Science & eng"),
        ("Sc", "Social sciences"),
    ]
    role = models.CharField(max_length=255, choices=ROLE,default="participant")
    affiliation = models.CharField(max_length=255)
    email=models.EmailField(unique=True,validators=[verifyemail])
    nationality = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
        if not(self.user_id):
            newid=generate_user_id()
            while User.objects.filter(user_id=newid).exists():
                newid=generate_user_id()
            self.user_id=newid
        super().save(*args,**kwargs)
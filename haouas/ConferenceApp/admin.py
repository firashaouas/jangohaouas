from django.contrib import admin
from .models import Conference
from .models import OrganizinCommitte  
from .models import Submission
from django.core.validators import FileExtensionValidator
import uuid

admin.site.site_title="gestion conference 25/26"
admin.site.site_header="gestion conference 25/26"
admin.site.index_title="django app"
# Register your models here.
def generate_sub_id():
   return "SUB-"+uuid.uuid4().hex[:8].upper()
file_validator=FileExtensionValidator(
   allowed_extensions=['pdf'],
   message="doit etre .pdf"
)
admin.site.register(Conference)
admin.site.register(OrganizinCommitte)
class SubmissionAdmin(admin.ModelAdmin):
    exclude = ('submission_id', 'created_at', 'updated_at')  # on cache le champ

    def save_model(self, request, obj, form, change):
        if not obj.submission_id:
            obj.submission_id = generate_sub_id()
        super().save_model(request, obj, form, change)

admin.site.register(Submission, SubmissionAdmin)
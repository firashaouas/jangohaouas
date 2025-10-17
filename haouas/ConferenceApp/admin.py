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
#dmin.site.register(Conference)
admin.site.register(OrganizinCommitte)
class SubmissionAdmin(admin.ModelAdmin):
    exclude = ('submission_id', 'created_at', 'updated_at')
    actions = ["mark_as_payed", "reset_to_submitted"]
   

    def save_model(self, request, obj, form, change):
        if not obj.submission_id:
            obj.submission_id = generate_sub_id()
        super().save_model(request, obj, form, change)
    list_display=("title","status","user","payed","short_abstract",)
    list_filter=( "status","payed","conference","submission_date",)
    search_fields=("title","keywords",)
    list_editable=("status","payed",)
    readonly_fields=("submission_date","submission_id")
    fieldsets=(
        ("information",{
            "fields":( "submission_id", "title", "abstract", "keywords",)
        }),
        ("File",{
            "fields":( "paper", "conference",)
        }),
        ("Sui",{
            "fields":("status","payed","submission_date","user",)
        })


    )
    def short_abstract(self,object):
        if len(object.abstract) > 50:
            return object.abstract[:50]+'...'
        return object.abstract
    def mark_as_payed(self, request, queryset):
        updated = queryset.update(payed=True)
        self.message_user(request, f"{updated} soumission(s) ont été marquées comme payées")
    mark_as_payed.short_description = "Marquer comme payées"
    def reset_to_submitted(self, request, queryset):
        updated = queryset.update(status="submitted")
        self.message_user(request, f"{updated} soumission(s) ont été remises au statut 'submitted' ✅")

    reset_to_submitted.short_description = "Remettre au statut 'submitted'"


class AdminSubmission(admin.StackedInline):
    model=Submission
    extra=1
    readonly_fields=("submission_date","submission_id")
class AdminSubmissions(admin.TabularInline):
    model=Submission
    extra=1
    fields =("title","status","user","payed",)


admin.site.register(Submission, SubmissionAdmin)
@admin.register(Conference)
class AdminConferenceModel(admin.ModelAdmin):
    list_display=("name","theme","start_date","duration")

    ordering=("start_date",)
    list_filter=("theme","location",)
    search_fields=("description","name")
    fieldsets =(
        ("information",{
            "fields":("Conference_id","name","theme","description")
        }),
        ("logistics info",{
            "fields":("location","start_date","end_date")
        })
    )
    readonly_fields=("Conference_id",)
    def duration(self,objet):
        if objet.start_date and objet.end_date:
            return (objet.end_date-objet.start_date).days
        return "ras"
    duration.short_description="aaa"
    #inlines=[AdminSubmission]
    inlines=[AdminSubmissions]
    date_hierarchy="start_date"
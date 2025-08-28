from django.contrib import admin
from .models import Job, JobStatus

class JobStatusAdmin(admin.ModelAdmin):
    list_display = ['name']

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'content', 'job_link', 'company_link', 'applied_at', 'user']

admin.site.register(JobStatus, JobStatusAdmin)
admin.site.register(Job, JobAdmin)
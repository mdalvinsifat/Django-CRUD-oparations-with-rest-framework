from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.AvailableTime)

class SpecialaztionAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("title")}

admin.site.register(models.Designation)


admin.site.register(models.Specialization,SpecialaztionAdmin )
admin.site.register(models.Review)
admin.site.register(models.Doctor)

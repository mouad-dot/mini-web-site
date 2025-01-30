from django.contrib import admin
from mon_projet.models import Faculte, student, Cursus, Job, Employee, Campus

@admin.register(student)
class StudentAdmin(admin.ModelAdmin):
    filter_horizontal = ('amis',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    filter_horizontal = ('amis',)

admin.site.register(Faculte)
admin.site.register(Cursus)
admin.site.register(Job)
admin.site.register(Campus)

from django.contrib import admin
from.models import EmployeeMaster

# Register your models here.

class EmployeeMasterAdmin(admin.ModelAdmin):
    # Specify the ordering by fullname
    ordering = ['fullname']  # Order by fullname in ascending order

    # Optional: Specify which fields to display in the list view
    list_display = ('fullname', 'employee_code', 'email','role','warehouse', 'mobile')  # Add more fields as needed

# Register your model with the customized admin class
admin.site.register(EmployeeMaster, EmployeeMasterAdmin)
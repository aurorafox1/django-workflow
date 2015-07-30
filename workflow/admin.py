from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class FlowNameAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "type", "diagrams", "desc"]

class FlowStatusAdmin(admin.ModelAdmin):
    list_display = ["id", "flowname", "name", "desc"]

class FlowPermsAdmin(admin.ModelAdmin):
    list_display = ["id", "flowname", "flowstep"]

class FlowTransAdmin(admin.ModelAdmin):
    list_display = ["id", "flowname", "flowstep", "condition", "transtion"]
	
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'url', 'icon']

class UserExtAdmin(admin.TabularInline):
    model = UserExt

class userAdmin(UserAdmin):
    inlines = [UserExtAdmin]

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'desc']

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'desc']	


# Register your models here.
admin.site.register(FlowOpera)
admin.site.register(FlowName, FlowNameAdmin)
admin.site.register(FlowStatus, FlowStatusAdmin)
admin.site.register(FlowTrans, FlowTransAdmin)
admin.site.register(FlowPerms, FlowPermsAdmin)
admin.site.register(FlowRecord)
admin.site.unregister(User)
admin.site.register(Menu, MenuAdmin)
admin.site.register(User, userAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(Department, DepartmentAdmin)
from django.contrib import admin
from models import *
from forms import AdminItemForm


class ItemsAdmin(admin.ModelAdmin):
    form = AdminItemForm


# Register your models here.
admin.site.register(DdsItemGroups)
admin.site.register(DdsItems, ItemsAdmin)
admin.site.register(DdsAccountTypes)
admin.site.register(DdsAccounts)
admin.site.register(DdsFlow)

from django.contrib import admin

from glue.admin import RelatedContentInline
from genericadmin.admin import GenericAdminModelAdmin

from .models import Data

@admin.register(Data)
class DataAdmin(GenericAdminModelAdmin):
    inlines = [RelatedContentInline]

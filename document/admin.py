from django.contrib import admin
from .models import Document, Source
# Register your models here.

'''
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date', 'time', 'status',)
'''

admin.site.register(Document)
admin.site.register(Source)

# path/to/your/admin.py
from django.contrib import admin
from .models import App,AppCategory,AppChangelog,AppComment,AppTag  # Import your custom user model
from unfold.admin import ModelAdmin,TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget,ArrayWidget
from django.db import models
from django.contrib.postgres.fields import ArrayField
from unfold.contrib.import_export.forms import  ImportForm, SelectableFieldsExportForm
from import_export.admin import ImportExportModelAdmin

class AppChangelogInline(TabularInline):
    model = AppChangelog
    extra = 1
class AppCommentInline(TabularInline):
    model = AppComment
    extra = 1
@admin.register(App)
class AppAdmin(ModelAdmin,ImportExportModelAdmin):
    inlines = [AppChangelogInline,AppCommentInline]
    list_display = ('name', 'description','author','category','download_count')
    list_filter = ('name', 'description','author','category','download_count')
    search_fields = ('name', 'description','author','category','download_count')
    sortable_by = ('name', 'description','author','category','download_count')
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        }
    }

    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm  
    autocomplete_fields = ['tags']
@admin.register(AppTag)
class AppTagAdmin(ModelAdmin):
    model = AppTag
    extra = 1
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
        ArrayField: {
            "widget": ArrayWidget,
        }
    }
    search_fields = ('name',)

@admin.register(AppCategory)
class AppCategoriesAdmin(ModelAdmin):
    model = AppCategory
    extra = 1

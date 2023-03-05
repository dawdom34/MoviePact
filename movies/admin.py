from django.contrib import admin
from .models import MovieModel


class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'release_date', 'duration')
    search_fields = ('title', 'category', 'age_category', 'duration')
    readonly_fields = ('id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(MovieModel, MoviesAdmin)
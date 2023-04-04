from django.contrib import admin
from .models import MovieModel, ProgramModel, SeatsModel, TicketsModel


class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'release_date', 'duration')
    search_fields = ('title', 'category', 'age_category', 'duration')
    readonly_fields = ('id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(MovieModel, MoviesAdmin)


class ProgramAdmin(admin.ModelAdmin):
    list_display = ('movie', 'date', 'price')
    search_fields = ('movie', 'date', 'price')
    readonly_fields = ('id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(ProgramModel, ProgramAdmin)


class SeatsAdmin(admin.ModelAdmin):
    list_display = ('program', 'seats_numbers')
    search_fields = ('program', 'seats_numbers')
    readonly_fields = ('id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(SeatsModel, SeatsAdmin)


class TicketsAdmin(admin.ModelAdmin):
    list_display = ('program', 'user', 'seats')
    search_fields = ('program', 'user', 'seats')
    readonly_fields = ('id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(TicketsModel, TicketsAdmin)
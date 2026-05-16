from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import HeroSlide


@admin.register(HeroSlide)
class HeroSlideAdmin(ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Контент первого экрана', {
            'fields': ('eyebrow', 'title', 'subtitle', 'image'),
        }),
        ('Кнопки', {
            'fields': (
                ('primary_button_text', 'primary_button_url'),
                ('secondary_button_text', 'secondary_button_url'),
            ),
        }),
        ('Показ', {
            'fields': ('is_active', 'order'),
        }),
    )
    search_fields = ('title',)

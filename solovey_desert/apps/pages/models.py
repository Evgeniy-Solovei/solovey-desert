from django.db import models


class HeroSlide(models.Model):
    eyebrow = models.CharField('Надзаголовок', max_length=120, blank=True, default='БУТИК ДЕСЕРТОВ')
    title = models.CharField('Заголовок', max_length=220)
    subtitle = models.TextField('Текст', blank=True)
    image = models.ImageField('Фото для слайдера', upload_to='hero/')
    primary_button_text = models.CharField('Текст основной кнопки', max_length=80, blank=True, default='Смотреть каталог')
    primary_button_url = models.CharField('Ссылка основной кнопки', max_length=220, blank=True, default='#catalog')
    secondary_button_text = models.CharField('Текст второй кнопки', max_length=80, blank=True, default='Оставить заявку')
    secondary_button_url = models.CharField('Ссылка второй кнопки', max_length=220, blank=True, default='#order')
    is_active = models.BooleanField('Активен', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Слайд первого экрана'
        verbose_name_plural = 'Слайды первого экрана'

    def __str__(self):
        return self.title

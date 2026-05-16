from django.conf import settings


def site_settings(request):
    return {
        'site_url': settings.SITE_URL,
        'site_name': settings.SITE_NAME,
        'site_description': settings.SITE_DESCRIPTION,
        'site_phone': settings.SITE_PHONE,
        'site_email': settings.SITE_EMAIL,
        'site_city': settings.SITE_CITY,
        'yandex_metrica_id': settings.YANDEX_METRICA_ID,
        'yandex_webmaster_verification': settings.YANDEX_WEBMASTER_VERIFICATION,
        'google_site_verification': settings.GOOGLE_SITE_VERIFICATION,
        'google_analytics_id': settings.GOOGLE_ANALYTICS_ID,
    }

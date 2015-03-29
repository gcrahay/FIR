from django.conf import settings

settings.INCIDENT_SHOW_NUMBER = getattr(settings, "INCIDENT_SHOW_NUMBER", False)
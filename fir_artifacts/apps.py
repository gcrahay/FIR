from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ArtifactsConfig(AppConfig):
    name = 'fir_artifacts'
    verbose_name = _('Artifacts')

    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        from fir_artifacts.artifacts import registry
        # Discover the artifact types
        autodiscover_modules('artifacts', register_to=registry)
        # Discover the artifact tools
        autodiscover_modules('artifacts_tools', register_to=registry.tools)
        # Prepare artifact tools according to settings
        registry.tools.parse_settings()



from __future__ import unicode_literals

from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.template import Template

from fir_artifacts.artifacts.tools.base import AbstractArtifactTool


class GenericLinkTool(AbstractArtifactTool):
    key = 'link'
    name = None
    url_template = None

    @classmethod
    def validate_specialization(cls, **kwargs):
        if 'name' not in kwargs or kwargs['name'] is None:
            return False
        if 'url_template' not in kwargs or kwargs['url_template'] is None:
            return False
        return True

    def tooltip(self, artifact):
        flat_context = self.get_context(artifact=artifact)
        url_template = Template(self.url_template)
        url = url_template.render(flat_context)
        return mark_safe("{link_title} <a href='{link}' target='_blank'>{artifact}</a>".format(
            link_title=_('{link_name} on'.format(link_name=self.name)),
            link=url,
            artifact=artifact.value
        ))

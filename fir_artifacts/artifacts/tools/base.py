from __future__ import unicode_literals

from django.template import RequestContext
from django.utils import six
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from django.template.loader import get_template
from django.template import Context


class ArtifactToolMeta(type):
    """
    Meta class for artifact tools:
    auto-registers the tool when discovered
    """
    def __new__(mcs, name, parents, attributes):
        from fir_artifacts.artifacts import registry
        klass = super(ArtifactToolMeta, mcs).__new__(mcs, name, parents, attributes)
        if attributes.get('artifact_type', None) is None and name != 'AbstractArtifactTool':
            registry.tools.register(klass)
        return klass


class AbstractArtifactTool(object):
    __metaclass__ = ArtifactToolMeta
    # ID of the tool (mandatory and unique)
    key = None
    # verbose name of the tool (unused and optional)
    name = "Base class for artifact tools"
    # compatible artifact types with this tool
    managed_artifacts = '__all__'
    # Django template for the static part
    static_template = None

    def __init__(self, artifact_type, related):
        self.artifact_type = artifact_type
        self.related = related

    def get_context(self, **kwargs):
        kwargs['related'] = self.related
        request = kwargs.pop('request', None)
        if request is None:
            context = Context(kwargs)
        else:
            context = RequestContext(request, kwargs)
        return context

    def get_static_template(self):
        if self.static_template is not None:
            return get_template(self.static_template)
        return None

    def static(self, request=None):
        template = self.get_static_template()
        if template is None:
            return ''
        context = self.get_context(request=request)
        return template.render(context)

    def extra(self, artifact):
        """
        Generates the extra part of the tool for an artifact object
        See `fir_artifacts_enrichement.artifacts_tools.EnrichedArtifactTool` for usage
        Args:
            artifact: artifact object

        Returns: an HTML string or None

        """
        return None

    def tooltip(self, artifact):
        """
        Generates the tooltip link of the tool for an artifact object
        Args:
            artifact: artifact object

        Returns: an HTML string or None

        """
        return ''

    @classmethod
    def _validate_specialization(cls, **kwargs):
        if isinstance(cls.managed_artifacts, six.string_types):
            if cls.managed_artifacts == '__all__':
                return cls.validate_specialization(**kwargs)
            else:
                cls.managed_artifacts = [cls.managed_artifacts, ]
        if 'artifact_type' in kwargs and kwargs['artifact_type'] is not None \
                and kwargs['artifact_type'].key in cls.managed_artifacts:
            return cls.validate_specialization(**kwargs)
        return False

    @classmethod
    def validate_specialization(cls, **kwargs):
        """ Override this class method to validate specialization parameters """
        return True

    @classmethod
    def specialize(cls, artifact_type, **kwargs):
        if cls == AbstractArtifactTool:
            raise ImproperlyConfigured(_("You must register a subclass of AbstractArtifactTool as an artifact tool."))
        kwargs['artifact_type'] = artifact_type
        if not cls._validate_specialization(**kwargs):
            raise ImproperlyConfigured(_('Wrong parameters or incompatible artifact type for {}'.format(cls.__name__)))
        name = cls.__name__
        if name.startswith('Generic'):
            name = name[7:]
        tool_type = ''.join(x.capitalize() or '_' for x in artifact_type.key.lower().split('_'))
        return type(b'{type}{name}'.format(name=name,  type=tool_type), (cls, ), kwargs)

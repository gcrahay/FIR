import re

from django.template import RequestContext
from django.template.loader import get_template

from fir_artifacts.artifacts.artifact_registry import registry
from fir_artifacts.signals import artifact_attached


class ArtifactMeta(type):
    def __new__(mcs, name, parents, attributes):
        from fir_artifacts.artifacts.artifact_registry import registry
        klass = super(ArtifactMeta, mcs).__new__(mcs, name, parents, attributes)
        if name != 'AbstractArtifact':
            registry.register(klass)
        return klass


class AbstractArtifact(object):
    __metaclass__ = ArtifactMeta
    case_sensitive = False
    template = 'fir_artifacts/default.html'

    @classmethod
    def find(cls, data):
        results = []
        for i in re.finditer(cls.regex, data):
            if cls.case_sensitive:
                results.append(i.group('search'))
            else:
                results.append(i.group('search').lower())

        return results


    @classmethod
    def _after_save(cls, value, event):
        artifact_attached.send(sender=event.__class__, key=cls.key, value=value, related=event)
        cls.after_save(value, event)

    @classmethod
    def after_save(cls, value, event):
        pass

    def __init__(self, artifacts, event, user=None):
        class ArtifactDisplay(object):
            def __init__(self, artifact, tools, user):
                self.artifact = artifact
                self.correlation_count = self.artifact.relations_for_user(user).count()
                self._tooltips = []
                self._extras = []
                for tool in tools:
                    tooltip = tool.tooltip(artifact)
                    if tooltip:
                        self._tooltips.append(tooltip)
                    extra = tool.extra(artifact)
                    if extra:
                        self._extras.append(extra)

            @property
            def value(self):
                return self.artifact.value

            @property
            def type(self):
                return self.artifact.type

            @property
            def id(self):
                return self.artifact.id

            @property
            def pk(self):
                return self.artifact.pk

            @property
            def tooltips(self):
                return self._tooltips

            def extras(self):
                return self._extras

        self._tools = []
        if len(artifacts):
            self._tools = [tool_class(artifacts[0].type, event) for tool_class in registry.tools.get(artifacts[0].type)]
        self._artifacts = [ArtifactDisplay(artifact, self._tools, user) for artifact in artifacts]
        self._event = event

        self._correlated = []
        for artifact in self._artifacts:
            if artifact.correlation_count > 1:
                self._correlated.append(artifact)

    def json(self, request):
        return self.display(request, correlated=False, json=True)

    def display(self, request, correlated=False, json=False):
        context = RequestContext(request)
        template = get_template(self.__class__.template)
        context['artifact_name'] = self.__class__.display_name
        if correlated:
            context['artifact_values'] = self._correlated
        else:
            context['artifact_values'] = self._artifacts

        context['event'] = self._event

        if not json:
            return template.render(context.flatten(), request)
        else:
            return context.flatten()

    def correlated_count(self):
        return len(self._correlated)

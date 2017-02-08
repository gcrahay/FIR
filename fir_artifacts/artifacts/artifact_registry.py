from django.conf import settings
from django.utils import six


class ArtifactRegistry(object):
    def __init__(self):
        self._registry = {}
        self._tools = None

    @property
    def tools(self):
        if self._tools is None:
            from fir_artifacts.artifacts.tools.tool_registry import ArtifactToolsRegistry
            self._tools = ArtifactToolsRegistry(self)
        return self._tools

    def register(self, *args):
        blacklist = getattr(settings, 'ARTIFACTS_DISABLED_TYPES', [])
        for artifact_class in args:
            if artifact_class.key not in blacklist:
                self._registry[artifact_class.key] = artifact_class

    def unregister(self, *args):
        for artifact_class_or_name in args:
            if not isinstance(artifact_class_or_name, six.string_types):
                artifact_class_or_name = artifact_class_or_name.key
            if artifact_class_or_name in self._registry:
                del self._registry[artifact_class_or_name]

    def search_from_relation(self, obj, user=None):
        result = []
        total_count = 0
        correlated_count = 0

        if not hasattr(obj, "artifacts"):
            return result, total_count, correlated_count

        for artifact_type, artifact_class in self._registry.items():
            values = obj.artifacts.filter(type=artifact_type)
            artifact_collection = artifact_class(values, obj, user=user)
            total_count += values.count()
            correlated_count += artifact_collection.correlated_count()
            result.append(artifact_collection)

        return result, total_count, correlated_count

    @staticmethod
    def search_related_from_string(artifact_string):
        from fir_artifacts.models import Artifact
        artifacts = Artifact.objects.filter(value__contains=artifact_string)
        incs = []
        for a in artifacts:
            incs.extend(a.relations.all())
        return incs

    def extract(self, data):
        from fir_artifacts.models import ArtifactBlacklistItem

        result = dict()
        for artifact_type, artifact_class in self._registry.items():
            blacklist = ArtifactBlacklistItem.objects.filter(type=artifact_type).values_list('value', flat=True)
            values = artifact_class.find(data)
            values = [v for v in values if v not in blacklist]
            result[artifact_type] = values

        return result

    def after_save(self, artifact_type, artifact_value, related):
        self._registry[artifact_type]._after_save(artifact_value, related)


registry = ArtifactRegistry()

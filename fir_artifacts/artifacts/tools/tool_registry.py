from django.utils import six


class ArtifactToolsRegistry(object):
    def __init__(self, artifact_registry):
        self._registry = {}
        self._artifacts = artifact_registry
        self._artifact_tools = {}

    def register(self, *args):
        for tool_class in args:
            if tool_class.key is not None:
                self._registry[tool_class.key] = tool_class

    def unregister(self, *args):
        for tool_class_or_name in args:
            if not isinstance(tool_class_or_name, six.string_types):
                tool_class_or_name = tool_class_or_name.key
            if tool_class_or_name in self._registry:
                del self._registry[tool_class_or_name]

    def parse_settings(self):
        from django.conf import settings
        tools_setting = getattr(settings, 'ARTIFACTS_TOOLS', {})
        for artifact_type, tools in tools_setting.items():
            if artifact_type not in self._artifacts._registry:
                continue
            artifact_class = self._artifacts._registry[artifact_type]
            for tool in tools:
                if isinstance(tool, six.string_types):
                    tool_name = tool
                    tool = {}
                else:
                    tool_name = tool.pop('tool', None)
                if tool_name is not None and tool_name in self._registry:
                    if artifact_type not in self._artifact_tools:
                        self._artifact_tools[artifact_type] = []
                    self._artifact_tools[artifact_type].append(self._registry[tool_name].specialize(artifact_class, **tool))

    def get(self, artifact_type):
        return self._artifact_tools.get(artifact_type, [])

from fir_artifacts.artifacts import AbstractArtifact


class MAC(AbstractArtifact):
    key = 'mac'
    display_name = 'MACs'
    regex = r'(([^a-fA-F0-9])|^)(?P<search>(?:[a-fA-F0-9]{2}[:|\-]){5}[a-fA-F0-9]{2})(([^a-fA-F0-9])|$)'

    @classmethod
    def find(cls, data):
        # MAC address normalization: hyphen as separator
        results = super(MAC, cls).find(data)
        return [r.replace(':', '-') for r in results]

from fir_artifacts.artifacts import AbstractArtifact


class CommonVulnerabilityAndExposure(AbstractArtifact):
    key = 'cve'
    display_name = 'CVE IDs'
    regex = r"(?P<search>[Cc][Vv][Ee]-[0-9]{4}-[0-9]{4,})"

    @classmethod
    def find(cls, data):
        results = super(CommonVulnerabilityAndExposure, cls).find(data)
        return [r.upper() for r in results]


class CommonWeaknessEnumeration(AbstractArtifact):
    key = 'cwe'
    display_name = 'CWE IDs'
    regex = r"(?P<search>[Cc][Ww][Ee]-[0-9]{1,})"

    @classmethod
    def find(cls, data):
        results = super(CommonWeaknessEnumeration, cls).find(data)
        return [r.upper() for r in results]

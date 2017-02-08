from django.template.loader import get_template
from django.utils.safestring import mark_safe
from fir_artifacts.artifacts.tools.base import AbstractArtifactTool


class EnrichedArtifactTool(AbstractArtifactTool):
    key = 'enriched_artifact'
    managed_artifacts = ['hostname', 'email', 'ip', 'url']

    def extra(self, artifact):
        from fir_artifacts_enrichment.models import ArtifactEnrichment
        enrichments = ArtifactEnrichment.objects.filter(artifact_id=artifact.id)
        if not enrichments.exists():
            return None
        template = get_template('fir_artifacts_enrichment/panel_tool.html')
        return template.render(self.get_context(enrichments=enrichments, artifact=artifact).flatten())

    def tooltip(self, artifact):
        from fir_artifacts_enrichment.models import ArtifactEnrichment
        enrichments = ArtifactEnrichment.objects.filter(artifact_id=artifact.id)
        if not enrichments.exists():
            return None
        return mark_safe(
            "<a href='#' data-toggle='modal' data-target='#enriched-artifact-{artifact_id}-modal'>Enrichment</a>".format(
                artifact_id=artifact.id))

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, render

from fir_artifacts import artifacts as libartifacts

from incidents.models import Incident
from incidents.views import is_incident_handler


@login_required
@user_passes_test(is_incident_handler)
def list(request, event_id):
    i = get_object_or_404(Incident, pk=event_id)

    (artifacts, artifacts_count, correlated_count) = libartifacts.all_for_event(i)


    return render(request, "fir_artifacts/list.html", {"event": i,
                                                  'correlated_count': correlated_count,
                                                  'artifacts_count': artifacts_count,
                                                  'artifacts': artifacts,
    })

@login_required
@user_passes_test(is_incident_handler)
def correlation(request, event_id):
    i = get_object_or_404(Incident, pk=event_id)

    (artifacts, artifacts_count, correlated_count) = libartifacts.all_for_event(i)


    return render(request, "fir_artifacts/correlation.html", {"event": i,
                                                  'correlated_count': correlated_count,
                                                  'artifacts_count': artifacts_count,
                                                  'artifacts': artifacts,
    })
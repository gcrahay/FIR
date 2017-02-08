from django.dispatch import Signal

artifact_attached = Signal(providing_args=['key', 'value', 'related'])
artifact_detached = Signal(providing_args=['key', 'value', 'related'])

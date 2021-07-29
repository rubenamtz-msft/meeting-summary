from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SummaryConfig(AppConfig):
    name = 'meeting_summary.summary'
    verbose_name = _("summary")

    def ready(self):
        try:
            import meeting_summary.summary.signals  # noqa F401
        except ImportError:
            pass

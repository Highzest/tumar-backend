from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommunityConfig(AppConfig):
    name = "tumar.community"
    verbose_name = _("Community")

#########################################################################
from __future__ import print_function, unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

#########################################################################


class MailingListConfig(AppConfig):
    name = "maillist"
    verbose_name = _("Mailing lists")

    def ready(self):
        """
        Any app specific startup code, e.g., register signals,
        should go here.
        """


#########################################################################

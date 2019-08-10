"""
This script is run periodically throughout the year.
Its purpose is to generate local mailing list information for distribution
to another MTA.


"""
############################################################################
from __future__ import print_function, unicode_literals

import os
import sys
import traceback

from django.conf import settings

from ..models import MailingList

# Setup Django environment
DJANGO_COMMAND = "generate_entrypoint"
OPTION_LIST = (
    (
        ["--pickle"],
        dict(
            action="store_true",
            help="When this option is given, the script outputs a pickle",
        ),
    ),
)
HELP_TEXT = "Generate mailing lists info for remote MTA (cron)"
ARGS_USAGE = "[--pickle]"


############################################################################


############################################################################


def main():
    data = {}
    for maillist in MailingList.objects.active():
        address_list = list(
            maillist.member_set.active().values_list("email", flat=True)
        )
        data[maillist.slug] = ",".join(address_list)
    return data


############################################################################


def generate_entrypoint(options, args):
    d = main()
    if "pickle" in options and options["pickle"]:
        # cron, etc.
        import cPickle

        sys.stdout.write(cPickle.dumps(d))
    else:
        # interactive
        import pprint

        pprint.pprint(d)
        if len(d) > 0:
            print(max([len(dest) for dest in d.values()]))
        else:
            print("NO RESULTS!")


############################################################################
#

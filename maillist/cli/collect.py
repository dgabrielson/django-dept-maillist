"""
This script is run periodically throughout the year.
Its purpose is to keep all departmental email addresses/lists up to date.


----------------------

This will scan all apps for a utils/EMAIL.py module.
If found, this module will be loaded (utils/__init__.py must exist!)
and its main() function executed.

Each of these main functions must return a dictionary of no-domain addresses
mapping to receipients.  These addresses will be updated on the mail server
as necessary.  The dictionary may be empty, but the return value MUST be
a dictionary.

"""
############################################################################
from __future__ import print_function, unicode_literals

import os
import sys
import traceback

from django.apps.registry import apps
from django.conf import settings

from ..models import MailingList

############################################################################

# Setup Django environment
DJANGO_COMMAND = "collect_entrypoint"
USE_ARGPARSE = True
OPTION_LIST = (
    (
        ["-x", "--exclude"],
        {"action": "append", "help": "List of applications to exclude"},
    ),
)
HELP_TEXT = "Collect mailing list information from installed applications (cron)"
ARGS_USAGE = ""

############################################################################


def main(options):
    verbosity = int(options.get("verbosity"))
    exclude_list = options.get("exclude")
    if exclude_list is None:
        exclude_list = []
    results = {}
    for app in apps.get_app_configs():
        if app.name in exclude_list:
            if verbosity > 2:
                print("excluding:", app.name)
            continue
        if verbosity > 2:
            print("trying:", app.name)
        try:
            m = __import__("%s.utils.EMAIL" % app.name)
        except ImportError:
            pass  # no email generator for this app
        else:
            if verbosity > 1:
                print("collecting from:", app.name)
            try:
                d = m.utils.EMAIL.main()
            except:
                print("-" * 25)
                print("APPLICATION:", app.name)
                traceback.print_exc()
                print("=" * 50)
            else:
                for key, data in d.items():
                    if verbosity > 2:
                        print("({}, {}) = {}".format(app.name, key, data))
                    results[(app.name, key)] = data

    # Fix 'safe strings' Django-ism.
    uni_res = {}
    deactivate = []
    for key, value in results.items():
        if value is None:
            if verbosity > 2:
                print("flagging", key, "for deativation")
            deactivate.append(key)
        else:
            uni_res[key] = value
    return uni_res, deactivate


############################################################################


def collect_entrypoint(options, args):
    data, deactivate = main(options)
    verbosity = int(options.get("verbosity"))
    # database update:
    for key in data:
        app, slug = key
        maillist = MailingList.objects.get_from_slug(slug)
        if not maillist.active:
            maillist.active = True
            maillist.save()
        address_list = list(
            maillist.member_set.automatic().values_list("email", flat=True)
        )
        for addr in data[key].split(","):
            maillist.add_member(addr, automatic=True)
            if addr in address_list:
                address_list.remove(addr)

        for addr in address_list:
            maillist.remove_member(addr)

    for app, slug in deactivate:
        maillist_qs = MailingList.objects.filter(slug=slug, active=True)
        if maillist_qs.exists():
            maillist = maillist_qs.get()
            maillist.active = False
            maillist.save()
            maillist.member_set.all().delete()


############################################################################
#

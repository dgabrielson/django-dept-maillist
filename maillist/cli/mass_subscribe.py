"""
Mass subscribe to an email list.
"""
############################################################################
from __future__ import print_function, unicode_literals

import os
import sys
import traceback

from django.conf import settings
from django.utils import six

from ..models import MailingList
from ..utils import get_bulk_add_email_addresses

# Setup Django environment
DJANGO_COMMAND = "main"
OPTION_LIST = ((["slug"], {"help": "List slug to subscribe"}),)
USE_ARGPARSE = True
HELP_TEXT = "Mass subscribe manual entries to a mailing list"
ARGS_USAGE = "[list-slug]"


############################################################################


############################################################################


def mass_subscribe(list_slug, text):
    maillist = MailingList.objects.active().get(slug=list_slug)
    if isinstance(text, six.string_types):
        raw_email_list = get_bulk_add_email_addresses(text)
    else:
        raw_email_list = text  # assume pre-processed list.
    for email in raw_email_list:
        maillist.add_member(email)


############################################################################


def main(options, args):
    list_slug = options["slug"]
    if sys.stdin.isatty():
        print(
            "Enter email addresses as address@example.com, Name <a@e.c>, or a@e.c (Name)"
        )
        print("One address per line, CTRL+D when done")
        print()

    text = sys.stdin.read()
    mass_subscribe(list_slug, text)


############################################################################
#

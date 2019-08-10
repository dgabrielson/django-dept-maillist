"""
CLI list for mailing list members.
"""
#######################################################################
#######################################################################
from __future__ import print_function, unicode_literals

from ..models import Member as Model
from . import resolve_fields

HELP_TEXT = __doc__.strip()
DJANGO_COMMAND = "main"
OPTION_LIST = (
    (
        ["-f", "--fields"],
        dict(
            dest="field_list",
            help="Specify a comma delimited list of fields to include, e.g., -f PROVIDE,EXAMPLE",
        ),
    ),
)


#######################################################################


#######################################################################


def main(options, args):
    if not options["field_list"]:
        options["field_list"] = "list.slug"
    qs = Model.objects.active()
    for item in qs:
        value_list = ["{}".format(item.pk), "{}".format(item)]
        if options["field_list"]:
            value_list += resolve_fields(item, options["field_list"].split(","))
        print("\t".join(value_list))


#######################################################################

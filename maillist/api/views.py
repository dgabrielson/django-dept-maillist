###############################################################
from __future__ import print_function, unicode_literals

from maillist.models import MailingList, Member
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import MailingListSerializer, MemberSerializer

###############################################################


class MaillistPermissions(object):
    """
    Permission class mixin for all Mailing list Views/ViewSets.
    """

    permission_classes = (permissions.IsAdminUser, permissions.DjangoModelPermissions)


###############################################################


class MaillistModelViewSet(MaillistPermissions, viewsets.ModelViewSet):
    """
    Base class for all Maillist viewsets
    """


###############################################################


class MailingListViewSet(MaillistModelViewSet):
    queryset = MailingList.objects.all()
    serializer_class = MailingListSerializer


###############################################################


class MemberViewSet(MaillistModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


###############################################################

###############################################################
from __future__ import print_function, unicode_literals

from maillist.models import MailingList, Member
from rest_framework import serializers

###############################################################


class MemberInlineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ("url", "email")


class MemberSerializer(MemberInlineSerializer):
    class Meta:
        model = Member
        fields = ("url", "active", "created", "modified", "list", "email", "automatic")


###############################################################


class MailingListSerializer(serializers.HyperlinkedModelSerializer):
    #     member_set = MemberInlineSerializer(many=True)

    class Meta:
        model = MailingList
        fields = (
            "url",
            "active",
            "created",
            "modified",
            "slug",
            "verbose_name",
            "description",
            "member_set",
        )


###############################################################

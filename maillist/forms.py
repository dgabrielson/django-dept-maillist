"""
Forms for Mailing list application.
"""
################################################################
from __future__ import print_function, unicode_literals

from django import forms
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail

from .models import MailingList
from .utils import get_bulk_add_email_addresses

################################################################

DjangoUser = get_user_model()

################################################################


class AdminEmailForm(forms.Form):
    """
    A form for composing an email.
    Assumes that the from and the to will be given.
    """

    to_list = forms.ModelMultipleChoiceField(
        queryset=MailingList.objects.active(),
        widget=FilteredSelectMultiple("Receipents", False),
    )
    from_user = forms.ModelChoiceField(
        queryset=DjangoUser.objects.all(), widget=forms.HiddenInput
    )
    subject = forms.CharField(
        max_length=128, widget=forms.TextInput(attrs={"size": 90})
    )
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 18, "cols": 65}))

    @property
    def media(self):
        js = [
            "jquery.js",
            "jquery.init.js",
            "core.js",
            "SelectBox.js",
            "SelectFilter2.js",
        ]
        return forms.Media(js=[static("admin/js/%s" % path) for path in js])

    def send_email(self):
        """
        The form is assumed to be valid at the point this is called.
        Return the number of messages sent.
        """
        from_user = self.cleaned_data["from_user"]
        to_list = self.cleaned_data["to_list"]
        from_email = from_user.get_full_name() + " <" + from_user.email + ">"
        subject = self.cleaned_data["subject"]
        message = self.cleaned_data["message"]

        count = 0
        for mailinglist in to_list:
            for member in mailinglist.member_set.active():
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=from_email,
                    to=[member.email],
                )
                count += email.send()
        return count


################################################################


class AdminBulkSubscribeForm(forms.Form):
    """
    A form for bulk subscribing emails to a list.
    Assumes that the from and the to will be given.
    """

    mailinglist = forms.ModelChoiceField(
        queryset=MailingList.objects.active(), widget=forms.HiddenInput
    )
    email_addresses = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 25, "cols": 65}), help_text="One per line"
    )

    @property
    def media(self):
        js = [
            "jquery.js",
            "jquery.init.js",
            "core.js",
            "SelectBox.js",
            "SelectFilter2.js",
        ]
        return forms.Media(js=[static("admin/js/%s" % path) for path in js])

    def clean_email_addresses(self):
        text = self.cleaned_data["email_addresses"]
        try:
            raw_email_list = get_bulk_add_email_addresses(text)
        except Exception as e:
            raise ValidationError("{}".format(e))
        return text

    def bulk_subscribe(self):
        """
        The form is assumed to be valid at the point this is called.
        Return the number of email addresses subscribed
        """
        maillist = self.cleaned_data["mailinglist"]
        text = self.cleaned_data["email_addresses"]
        raw_email_list = get_bulk_add_email_addresses(text)
        count = 0
        for email in raw_email_list:
            maillist.add_member(email)
            count += 1
        return count


################################################################

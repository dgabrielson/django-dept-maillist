"""
Views for the Mailing list application.

Right now this entirely centers on the email_maillist view, which is 
available as an admin action.
"""
################################################################
from __future__ import print_function, unicode_literals

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import AdminBulkSubscribeForm, AdminEmailForm
from .models import MailingList

################################################################


class AdminSiteViewMixin(object):
    def get_admin_options(self):
        return self.kwargs.get("admin_options", None)

    def get_context_data(self, **kwargs):
        """
        Extend the context so the admin template works properly.
        """
        context = super(AdminSiteViewMixin, self).get_context_data(**kwargs)
        admin_options = self.get_admin_options()
        context.update(
            admin_options.admin_site.each_context(self.request),
            model=admin_options.model,
            opts=admin_options.model._meta,
            app_label=admin_options.model._meta.app_label,
        )
        return context


################################################################


class SendmailFormView(AdminSiteViewMixin, FormView):
    """
    A view for the admin to email Users as an action.
    """

    template_name = "admin/maillist/mailinglist/extra_form.html"
    form_class = AdminEmailForm

    def get_initial(self):
        """
        Get initial data for the form.
        """
        initial = super(SendmailFormView, self).get_initial()
        initial["from_user"] = self.request.user
        return initial

    def form_valid(self, form):
        """
        Process successful form submission.
        """
        n = form.send_email()
        suffix = "s" if n != 1 else ""
        msg = "Email has been sent to {0} recipient{1}.".format(n, suffix)
        messages.success(self.request, msg, fail_silently=True)
        return super(SendmailFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Extend the context so the admin template works properly.
        """
        context = super(SendmailFormView, self).get_context_data(**kwargs)
        context.update(
            submit_button_label="Send Email", page_header="Compose email message"
        )
        return context


################################################################


class EmailUsersAdminAction(SendmailFormView):
    """
    A view for the admin to email Users as an action.
    """

    success_url = reverse_lazy("admin:maillist_mailinglist_changelist")

    def get_initial(self):
        """
        Get initial data for the form.
        """
        initial = super(EmailUsersAdminAction, self).get_initial()

        selected = self.request.GET.getlist("to") if "to" in self.request.GET else []
        # to_list = LdapUser.objects.filter(pk__in=selected)
        initial["to_list"] = selected
        return initial


################################################################


class MailingListFormMixin(object):

    _mailinglist_cache = None

    def get_mailinglist(self):
        if self._mailinglist_cache is not None:
            return self._mailinglist_cache
        pk = self.kwargs.get("pk", None)
        obj = get_object_or_404(MailingList, pk=pk)
        self._mailinglist_cache = obj
        return obj

    def get_success_url(self):
        mailinglist = self.get_mailinglist()
        return mailinglist.admin_change_link()

    def get_context_data(self, **kwargs):
        """
        Extend the context so the admin template works properly.
        """
        context = super(MailingListFormMixin, self).get_context_data(**kwargs)
        context.update(original=self.get_mailinglist())
        return context


################################################################


class EmailMailingListAdminForm(MailingListFormMixin, SendmailFormView):
    """
    A view for the admin to email a particular list
    """

    def get_form(self, *args, **kwargs):
        form = super(EmailMailingListAdminForm, self).get_form(*args, **kwargs)
        # swap out the widget for the to_list:
        form.fields["to_list"].widget = form.fields["to_list"].hidden_widget()
        return form

    def get_initial(self):
        """
        Get initial data for the form.
        """
        initial = super(EmailMailingListAdminForm, self).get_initial()
        initial["to_list"] = [self.get_mailinglist()]
        return initial


################################################################


class BulkSubscribeAdminForm(AdminSiteViewMixin, MailingListFormMixin, FormView):
    """
    A view to bulk subscribe a mailing list.
    """

    template_name = "admin/maillist/mailinglist/extra_form.html"
    form_class = AdminBulkSubscribeForm

    def get_initial(self):
        """
        Get initial data for the form.
        """
        initial = super(BulkSubscribeAdminForm, self).get_initial()
        initial["mailinglist"] = self.get_mailinglist()
        return initial

    def form_valid(self, form):
        """
        Process successful form submission.
        """
        n = form.bulk_subscribe()
        suffix = "es" if n != 1 else ""
        msg = "Successfully subscribed {0} address{1}.".format(n, suffix)
        messages.success(self.request, msg, fail_silently=True)
        return super(BulkSubscribeAdminForm, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Extend the context so the admin template works properly.
        """
        context = super(BulkSubscribeAdminForm, self).get_context_data(**kwargs)
        context.update(submit_button_label="Subscribe", page_header="Bulk Subscribe")
        return context


################################################################

"""
Admin classes for the Mailing list application
"""
#########################################################
from __future__ import print_function, unicode_literals

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import MailingList, Member
from .views import (
    BulkSubscribeAdminForm,
    EmailMailingListAdminForm,
    EmailUsersAdminAction,
)

#########################################################


class MemberInline(admin.TabularInline):
    model = Member
    extra = 0


class MailingListAdmin(admin.ModelAdmin):
    """
    Mailing list admin interface.
    """

    actions = ["email_users_action"]
    inlines = [MemberInline]
    list_display = ["slug", "verbose_name"]
    prepopulated_fields = {"slug": ("verbose_name",)}
    save_on_top = True
    search_fields = ["slug", "verbose_name", "member__email"]

    def get_urls(self):
        """
        Extend the admin urls for this model.
        Provide a link by subclassing the admin change_form,
        and adding to the object-tools block.
        """
        urls = super(MailingListAdmin, self).get_urls()
        urls = [
            url(
                r"^email-users/$",
                self.admin_site.admin_view(EmailUsersAdminAction.as_view()),
                name="maillist_sendmail_action",
                kwargs={"admin_options": self},
            ),
            url(
                r"^(?P<pk>.+)/email-users/$",
                self.admin_site.admin_view(EmailMailingListAdminForm.as_view()),
                name="maillist_mailinglist_sendmail",
                kwargs={"admin_options": self},
            ),
            url(
                r"^(?P<pk>.+)/bulk-add-users/$",
                self.admin_site.admin_view(BulkSubscribeAdminForm.as_view()),
                name="maillist_mailinglist_bulk_add",
                kwargs={"admin_options": self},
            ),
        ] + urls
        return urls

    def email_users_action(self, request, queryset):
        """
        Redirect to the actual view.
        """
        url = reverse_lazy("admin:maillist_sendmail_action")
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        query = "&".join(["to={0}".format(s) for s in selected])
        return HttpResponseRedirect(url + "?" + query)

    email_users_action.short_description = "Email selected list(s)"


admin.site.register(MailingList, MailingListAdmin)


#########################################################

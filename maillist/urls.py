from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import MailingList

urlpatterns = [
    url(
        r"^$",
        login_required(
            ListView.as_view(queryset=MailingList.objects.active().public())
        ),
        name="maillist-list",
    ),
    url(
        r"^(?P<slug>[\w-]+)/$",
        login_required(
            DetailView.as_view(queryset=MailingList.objects.active().public())
        ),
        name="maillist-detail",
    ),
]

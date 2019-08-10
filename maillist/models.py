"""
Models for the mailing list application.
"""
from __future__ import print_function, unicode_literals

from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible

#######################################################################
#######################################################################
#######################################################################


class CustomQuerySetManager(models.Manager):
    """
    Custom Manager for an arbitrary model, just a wrapper for returning
    a custom QuerySet
    """

    queryset_class = models.query.QuerySet

    def get_queryset(self):
        """
        Return the custom QuerySet
        """
        return self.queryset_class(self.model)


class CustomQuerySet(models.query.QuerySet):
    """
    Custom QuerySet.
    """

    def active(self):
        """
        Returns only the active items in this queryset
        """
        return self.filter(active=True)


#######################################################################
#######################################################################
#######################################################################


class MaillistBase(models.Model):
    """
    An abstract base class.
    """

    active = models.BooleanField(default=True)
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="creation time"
    )
    modified = models.DateTimeField(
        auto_now=True, editable=False, verbose_name="last modification time"
    )

    class Meta:
        abstract = True


#######################################################################
#######################################################################


class MailingListQuerySet(CustomQuerySet):
    def public(self):
        return self.filter(public=True)


#######################################################################


class MailingListManager(CustomQuerySetManager):
    """
    Manager for mailing lists.
    """

    queryset_class = MailingListQuerySet

    def get_from_slug(self, slug, **kwargs):
        """
        get_or_create - but if verbose name is not in the kwargs, add it.
        """
        if "verbose_name" not in kwargs:
            kwargs["verbose_name"] = slug.replace("-", " ").title()
        obj, created = self.get_or_create(slug=slug, defaults=kwargs)
        return obj


MailingListManager = MailingListManager.from_queryset(MailingListQuerySet)

###############################################


@python_2_unicode_compatible
class MailingList(MaillistBase):
    """
    Model for mailing lists.
    Currently, just a few things.
    """

    slug = models.SlugField(unique=True, max_length=64)
    verbose_name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=True)

    objects = MailingListManager()

    class Meta:
        base_manager_name = "objects"
        ordering = ("verbose_name",)

    def __str__(self):
        return self.verbose_name

    def get_absolute_url(self):
        return reverse("maillist-detail", kwargs={"slug": self.slug})

    def add_member(self, email_address, **kwargs):
        """
        Add an email address to this list.
        """
        if "list" in kwargs:
            del kwargs["list"]
        obj, created = Member.objects.get_or_create(
            email=email_address, list=self, defaults=kwargs
        )
        save_obj = False
        if not created:
            # update values from kwargs
            for f in kwargs:
                if getattr(obj, f) != kwargs[f]:
                    setattr(obj, f, kwargs[f])
                    save_obj = True
            if save_obj:
                obj.save()
        if created or save_obj:
            self.save()
        return obj

    def remove_member(self, email_address):
        """
        Remove an email address from this list.
        """
        membership = self.member_set.filter(email=email_address, list=self)
        if membership:
            member = membership.get()
            member.delete()
            self.save()

    def admin_change_link(self):
        return reverse("admin:maillist_mailinglist_change", args=[self.pk])

    @property
    def alias_string(self):
        member_qs = self.member_set.active().filter(list=self)
        email_list = member_qs.values_list("email", flat=True)
        return ",".join(email_list)

    @property
    def alias_string_length(self):
        return len(self.alias_string)


#######################################################################
#######################################################################
#######################################################################


class MemberQuerySet(CustomQuerySet):
    """
    QuerySets for Member objects.
    """

    def automatic(self):
        return self.filter(automatic=True)

    def manual(self):
        return self.filter(automatic=False)


###############################################


class MemberManager(CustomQuerySetManager):
    """
    Manager for mailing lists.
    """

    queryset_class = MemberQuerySet


MemberManager = MemberManager.from_queryset(MemberQuerySet)

###############################################


@python_2_unicode_compatible
class Member(MaillistBase):
    """
    Model for members of mailing lists.
    Currently, just an email address and an automatic flag.
    """

    list = models.ForeignKey(
        MailingList, on_delete=models.CASCADE, limit_choices_to={"active": True}
    )
    email = models.EmailField()
    automatic = models.BooleanField(default=False)

    objects = MemberManager()

    class Meta:
        unique_together = ("list", "email")
        base_manager_name = "objects"

    def __str__(self):
        return self.email


#######################################################################
#######################################################################
#######################################################################

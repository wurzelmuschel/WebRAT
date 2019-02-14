from django.db import models

# Create your models here.

class Tag(models.Model):
    """
    Objects based on this class represent a "Tag", a short word or text
    associated with a special meaning that can be linked to a Router object
    and provide a way to store additional information. Many Routers can
    share a Tag, and Routers can have many Tags "attached" to them.
    """

    text = models.CharField(max_length=64)
    description = models.TextField()
    # TODO: Fix creator attribute once WebRATUser is declared
    # creator = models.OneToOneField(WebRATUser)
    created = models.DateTimeField(auto_now_add=True)


class Router(models.Model):
    """
    Objects based on this class represent a "Router" or node in a Freifunk
    network. Data that is stored in the database using this class will come
    from a Meshviewer database and is not entered manually, except for certain
    attributes like tags, notes and owners. Only these attributes should be
    altered by the application, as any other attributes can/will be
    overwritten by another import from Meshviewer.
    """

    nodeid = models.CharField(max_length=12, primary_key=True)

    hostname = models.TextField()
    site_code = models.TextField()

    # TODO: Fix owners attribute once WebRATUser is declared
    # owners = models.ManyToManyField(WebRATUser)
    notes = models.TextField()
    tags = models.ManyToManyField(Tag)
    last_edit = models.DateTimeField(auto_now=True)
    # TODO: Fix last_editor attribute once WebRATUser is declared
    # last_editor = models.OneToOneField(WebRATUser)

    autoupdate_enabled = models.BooleanField()
    autoupdate_branch = models.TextField()
    firmware_base = models.TextField()
    firmware_release = models.TextField()
    model = models.TextField()

    last_import = models.DateTimeField(auto_now=True)
    first_import = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField()
    is_online = models.BooleanField()

    longitude = models.FloatField()
    latitude = models.FloatField()

    gateway = models.CharField(max_length=12)
    gateway_nexthop = models.CharField(max_length=12)
    ipaddress = models.GenericIPAddressField()

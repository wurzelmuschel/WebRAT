from django.db import models

from credentials.models import Credential


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


class Node(models.Model):
    """
    Objects based on this class represent a "Node" in a Freifunk network.
    Data that is stored in the database using this class will come from a
    Meshviewer database and is not entered manually, except for certain
    attributes like tags, notes and owners. Only these attributes should be
    altered by the application, as any other attributes can/will be
    overwritten by another import from Meshviewer.
    """

    nodeid = models.CharField(max_length=12, primary_key=True)

    hostname = models.TextField()
    site_code = models.TextField()

    notes = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    last_edit = models.DateTimeField(null=True)  # maybe null
    # TODO: Fix last_editor attribute once WebRATUser is declared
    # last_editor = models.OneToOneField(WebRATUser) # maybe null

    autoupdate_enabled = models.BooleanField(null=True)
    autoupdate_branch = models.TextField(null=True)
    firmware_base = models.TextField(null=True)
    firmware_release = models.TextField(null=True)
    model = models.TextField(null=True)

    last_import = models.DateTimeField(auto_now=True)
    first_import = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(null=True)
    is_online = models.BooleanField(null=True)

    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)

    gateway = models.CharField(max_length=12, null=True)
    gateway_nexthop = models.CharField(max_length=12, null=True)
    ipaddress = models.GenericIPAddressField()

    # TODO: Fix owners attribute once WebRATUser is declared
    # owners = models.ManyToManyField(WebRATUser) # maybe null
    credentials = models.ManyToManyField(Credential)

    def reboot(self):
        pass

    def enable_config_mode(self):
        pass

    def install_firmware(self):
        pass

    def add_credential(self):
        pass

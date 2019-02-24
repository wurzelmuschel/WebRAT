#
# utils.py
#
#   Contains utility functions that support WebRAT's "nodes" module.
#
#
#   Copyright (c) 2019, Christoph Haas
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice, this
#      list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER "AS IS" AND ANY EXPRESS
#   OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#   OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#   IN NO EVENT SHALL THE COPYRIGHT OWNER BE LIABLE FOR ANY DIRECT, INDIRECT,
#   INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#   POSSIBILITY OF SUCH DAMAGE.
#
#   The views and conclusions contained in the software and documentation are those
#   of the author and should not be interpreted as representing official policies,
#   either expressed or implied, of the Freifunk project.
#

import requests

from WebRAT.settings import WEBRAT_MESHVIEWER_URLS
from nodes.models import Node


def import_nodes_from_url(url: str):
    """
    Import a set of nodes from a Meshviewer-compatible list of nodes into
    the database. The list provided under the URL must be valid JSON and
    contain a "nodes" section, which in turn contains data about the different
    nodes.

    It is important that with each new Meshviewer release this code needs to
    be checked for compatibility. Changes to the JSON file format must result
    in this code being adapted to fit the new format (e.g. changes to filed
    names, removal of fields etc.)

    :param url:
    :return:
    """

    # Retrieve a JSON-file from the URL provided as a parameter and select the 'nodes' sub-document from it

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        json = response.json()['nodes']
    except:
        # TODO: Log error
        return

    # Extract the relevant data from each node entry and insert them into the database

    count = 0  # Count the number of entries in total
    new = 0  # Count the number of newly created entries
    skipped = 0  # Count the number of skipped entries due to purge period or supernode
    updated = 0  # Count the number of updated entries

    for node in json:
        count += 1

        # Filter out supernodes, which have the 'is_gateway' key set to 'true'

        if 'is_gateway' in node.keys() and node['is_gateway']:
            skipped += 1
            continue

        # Get the 'best' IP address to use for contacting the router. Routable addresses are preferred
        # over addresses starting with the fe80 prefix. If no valid addresses are found for a router,
        # the placeholder address of ::1 will be inserted to mark the router as unreachable.

        ipaddress = '::1'
        if 'addresses' in node.keys():
            for ip in node['addresses']:
                ipaddress = ip
                if not ipaddress.startswith('fe80'):
                    break  # IP address found which does not start with fe80

        # Get other relevant information about a node from the data provided in the JSON-file

        nodeid = node['node_id'] if 'node_id' in node.keys() else ''
        hostname = node['hostname'] if 'hostname' in node.keys() else ''
        site_code = node['site_code'] if 'site_code' in node.keys() else ''
        autoupdate_enabled = node['autoupdater']['enabled'] if (
                'autoupdater' in node.keys() and 'enabled' in node['autoupdater'].keys()) else None
        autoupdate_branch = node['autoupdater']['branch'] if (
                'autoupdater' in node.keys() and 'branch' in node['autoupdater'].keys()) else None
        firmware_base = node['firmware']['base'] if (
                'firmware' in node.keys() and 'base' in node['firmware'].keys()) else ''
        firmware_release = node['firmware']['release'] if (
                'firmware' in node.keys() and 'release' in node['firmware'].keys()) else ''
        model = node['model'] if 'model' in node.keys() else ''
        last_seen = node['lastseen'] if 'lastseen' in node.keys() else None
        is_online = node['is_online'] if 'is_online' in node.keys() else None
        latitude = node['location']['latitude'] if (
                'location' in node.keys() and 'latitude' in node['location'].keys()) else None
        longitude = node['location']['longitude'] if (
                'location' in node.keys() and 'longitude' in node['location'].keys()) else None
        gateway = node['gateway'] if 'gateway' in node.keys() else None
        gateway_nexthop = node['gateway_nexthop'] if 'gateway_nexthop' in node.keys() else None

        # TODO: Normalize MAC adresses for gateway and gateway_nexthop

        # TODO: What if a node has been renamed or moved from one site to another
        # several entries with same nodeid

        # TODO: Do not add/update nodes that have been down for a give period of time, use WEBRAT_PURGE_PERIOD setting

        # Update a node in the database with the data received or insert a new one if a router
        # does not yet exist for a given nodeid

        created = None
        try:
            _, created = Node.objects.update_or_create(nodeid=nodeid,
                                                       defaults={
                                                           'hostname': hostname,
                                                           'site_code': site_code,
                                                           'autoupdate_branch': autoupdate_branch,
                                                           'autoupdate_enabled': autoupdate_enabled,
                                                           'firmware_base': firmware_base,
                                                           'firmware_release': firmware_release,
                                                           'model': model,
                                                           'last_seen': last_seen,
                                                           'is_online': is_online,
                                                           'latitude': latitude,
                                                           'longitude': longitude,
                                                           'gateway': gateway,
                                                           'gateway_nexthop': gateway_nexthop,
                                                           'ipaddress': ipaddress,
                                                       })
        except:
            # TODO: Handle errors
            pass

        if created:
            new += 1
        else:
            updated += 1

    # TODO: Log numbers to logfile
    print("Records: {0} - New: {1} - Updated: {2} - Skipped: {3}".format(count, new, updated, skipped))


def import_nodes():
    """
    Imports all nodes from all URLs given in the settings.py parameter
    WEBRAT_MESHVIEWER_URLS. Errors will be reported as entries in the logfile.

    :return:
    """

    for sitecode in WEBRAT_MESHVIEWER_URLS:
        # TODO: Log "Importing nodes for site "sitecode" from "URL"
        print('Importing routers for site {0} from {1}'.format(sitecode, WEBRAT_MESHVIEWER_URLS[sitecode]))
        import_nodes_from_url(WEBRAT_MESHVIEWER_URLS[sitecode])
        # TODO: Log "Importing nodes for site "sitecode" done
        print('Importing for site {0} done'.format(sitecode))


def purge_nodes(days: int):
    """
    Delete nodess that have not been online for a given period of time.

    :return:
    """

    # TODO: implement function using last_seen attribute, log number to logfile
    pass

# TODO: Tests
# - bad url scheme
# - non-existent file on server
# - file is not json
# - timeout while fetching
# - database not available

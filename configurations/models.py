from io import StringIO

from fabric import Connection
from paramiko import RSAKey


class Configuration:
    """

    """

    def __init__(self, credential, node):
        """

        """
        self.credential = credential
        self.node = node
        self.config = {}
        self.config_current = False
        self.config_commands = {}

    def _run(self, command):
        if self.credential.key:
            # TODO: if self.credential.keytype == 'RSA':
            pk = RSAKey.from_private_key(StringIO(self.credential.key.decode()),
                                         password=self.credential.passphrase.decode())
            # TODO: elseif DSA, ...
            ca = {'pkey': pk}
        else:
            ca = {'password': self.credential.password.decode()}

        with Connection(host=self.node.ipaddress,
                        user=self.credential.username,
                        connect_kwargs=ca,
                        connect_timeout=5) as con:
            result = con.run(command, warn=True, pty=True)  # TODO: hide='both'
            print(command)
            return (result.stdout, result.stderr, result.exited)

    def read(self):
        """

        :return:
        """

        # uci

        (stdout, stderr, exitcode) = self._run('uci show')
        if not exitcode:
            for line in stdout.split('\n'):
                key, _, value = line.replace("\'", '').strip().partition('=')
                self.config[key] = value
                # TODO: Split multiple values per key into array/list

        # Hostname

        (stdout, _, _) = self._run('pretty-hostname')
        self.config['hostname'] = stdout.strip()

    def write(self):
        # TODO: multiple commands in a single batch
        # TODO: trigger "wifi" command centrally after all commands are executed
        if self.config_commands:
            for parameter in self.config_commands.keys():
                self._run(self.config_commands[parameter])

    def update(self):
        pass

    #
    # Configuration parameters exposed as properties
    #

    # TODO: Deal with non-existant keys when reading

    # --- 2.4 GHz channel ---

    def set_channel_24(self, channel):
        # TODO: Check range of channel
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11g':
                    self.config_commands[
                        'channel_24'] = 'uci set wireless.radio{0}.channel={1} && uci commit wireless && wifi'.format(i,
                                                                                                                      channel)
            except:
                continue

    def get_channel_24(self):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11g':
                    return int(self.config['wireless.radio{0}.channel'.format(i)])
            except:
                continue

    channel_24 = property(fset=set_channel_24, fget=get_channel_24)

    # --- 5 GHz channel ---

    def set_channel_5(self, channel):
        # TODO: Check range of channel
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11a':
                    self.config_commands[
                        'channel_5'] = 'uci set wireless.radio{0}.channel={1} && uci commit wireless && wifi'.format(i,
                                                                                                                     channel)
            except:
                continue

    def get_channel_5(self):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11a':
                    return int(self.config['wireless.radio{0}.channel'.format(i)])
            except:
                continue

    channel_5 = property(fset=set_channel_5, fget=get_channel_5)

    # --- 2.4 GHz client radio ---

    def set_client_radio_24(self, enable):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11g':
                    param = 0 if enable else 1  # reverse logic implemented by gluon!
                    self.config_commands[
                        'client_radio_24'] = 'uci set wireless.client_radio{0}.disabled={1} && uci commit wireless && wifi'.format(
                        i, param)
            except:
                continue

    def get_client_radio_24(self):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11g':
                    return '0' == self.config[
                        'wireless.client_radio{0}.disabled'.format(i)]  # reverse logic implemented by gluon!
            except:
                continue

    client_radio_24 = property(fset=set_client_radio_24, fget=get_client_radio_24)

    # --- 5 GHz client radio ---

    def set_client_radio_5(self, enable):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11a':
                    param = 0 if enable else 1  # reverse logic implemented by gluon!
                    self.config_commands[
                        'client_radio_5'] = 'uci set wireless.client_radio{0}.disabled={1} && uci commit wireless && wifi'.format(
                        i, param)
            except:
                continue

    def get_client_radio_5(self):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11a':
                    return '0' == self.config[
                        'wireless.client_radio{0}.disabled'.format(i)]  # reverse logic implemented by gluon!
            except:
                continue

    client_radio_5 = property(fset=set_client_radio_5, fget=get_client_radio_5)

    # --- 2.4 GHz mesh radio ---

    def set_mesh_radio_24(self, enable):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11g':
                    param = 0 if enable else 1  # reverse logic implemented by gluon!
                    self.config_commands[
                        'mesh_radio_24'] = 'uci set wireless.mesh_radio{0}.disabled={1} && uci commit wireless && wifi'.format(
                        i, param)
            except:
                continue

    def get_mesh_radio_24(self):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11g':
                    return '0' == self.config[
                        'wireless.mesh_radio{0}.disabled'.format(i)]  # reverse logic implemented by gluon!
            except:
                continue

    mesh_radio_24 = property(fset=set_mesh_radio_24, fget=get_mesh_radio_24)

    # --- 5 GHz mesh radio ---

    def set_mesh_radio_5(self, enable):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11a':
                    param = 0 if enable else 1  # reverse logic implemented by gluon!
                    self.config_commands[
                        'mesh_radio_5'] = 'uci set wireless.mesh_radio{0}.disabled={1} && uci commit wireless && wifi'.format(
                        i, param)
            except:
                continue

    def get_mesh_radio_5(self):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11a':
                    return '0' == self.config[
                        'wireless.mesh_radio{0}.disabled'.format(i)]  # reverse logic implemented by gluon!
            except:
                continue

    mesh_radio_5 = property(fset=set_mesh_radio_5, fget=get_mesh_radio_5)

    # --- 2.4 GHz htmode ---

    def set_htmode_24(self, htmode):
        # TODO: Check input (HT20, HT40, HT40+, HT40-, VHT20, VHT40, VHT80, VHT160 - https://oldwiki.archive.openwrt.org/doc/uci/wireless)
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11g':
                    self.config_commands[
                        'mesh_radio_24'] = "uci set wireless.radio{0}.htmode='{1}' && uci commit wireless && wifi".format(
                        i, htmode)
            except:
                continue

    def get_htmode_24(self):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11g':
                    return self.config['wireless.radio{0}.htmode'.format(i)]
            except:
                continue

    htmode_24 = property(fset=set_htmode_24, fget=get_htmode_24)

    # --- 5 GHz htmode ---

    def set_htmode_5(self, htmode):
        # TODO: Check input (HT20, HT40, HT40+, HT40-, VHT20, VHT40, VHT80, VHT160 - https://oldwiki.archive.openwrt.org/doc/uci/wireless)
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11a':
                    self.config_commands[
                        'mesh_radio_5'] = "uci set wireless.radio{0}.htmode='{1}' && uci commit wireless && wifi".format(
                        i, htmode)
            except:
                continue

    def get_htmode_5(self):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11a':
                    return self.config['wireless.radio{0}.htmode'.format(i)]
            except:
                continue

    htmode_5 = property(fset=set_htmode_5, fget=get_htmode_5)

    # --- 2.4 GHz country ---

    def set_country_24(self, country):
        # TODO: Check input
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11g':
                    self.config_commands[
                        'country_24'] = "uci set wireless.radio{0}.country='{1}' && uci commit wireless && wifi".format(
                        i, country)
            except:
                continue

    def get_country_24(self):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11g':
                    return self.config['wireless.radio{0}.country'.format(i)]
            except:
                continue

    country_24 = property(fset=set_country_24, fget=get_country_24)

    # --- 5 GHz country ---

    def set_country_5(self, country):
        # TODO: Check input
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11a':
                    self.config_commands[
                        'country_5'] = "uci set wireless.radio{0}.country='{1}' && uci commit wireless && wifi".format(
                        i, country)
            except:
                continue

    def get_country_5(self):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11a':
                    return self.config['wireless.radio{0}.country'.format(i)]
            except:
                continue

    country_5 = property(fset=set_country_5, fget=get_country_5)

    # --- 2.4 GHz txpower ---

    def set_txpower_24(self, txpower):
        # TODO: Check input
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11g':
                    self.config_commands[
                        'txpower_24'] = 'uci set wireless.radio{0}.txpower={1} && uci commit wireless && wifi'.format(i,
                                                                                                                      txpower)
            except:
                continue

    def get_txpower_24(self):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11g':
                    return int(self.config['wireless.radio{0}.txpower'.format(i)])
            except:
                continue

    txpower_24 = property(fset=set_txpower_24, fget=get_txpower_24)

    # --- 5 GHz txpower ---

    def set_txpower_5(self, txpower):
        # TODO: Check input
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11a':
                    self.config_commands[
                        'txpower_5'] = 'uci set wireless.radio{0}.txpower={1} && uci commit wireless && wifi'.format(i,
                                                                                                                     txpower)
            except:
                continue

    def get_txpower_5(self):
        for i in range(0, 10):
            try:
                if self.config['wireless.radio{0}.hwmode'.format(i)] == '11a':
                    return int(self.config['wireless.radio{0}.txpower'.format(i)])
            except:
                continue

    txpower_5 = property(fset=set_txpower_5, fget=get_txpower_5)

    ###

    # --- Hostname ---

    def set_hostname(self, hostname):
        if hostname:
            self.config_commands['hostname'] = 'pretty-hostname {0}'.format(hostname)

    def get_hostname(self):
        return self.config['hostname']

    hostname = property(fset=set_hostname, fget=get_hostname)

    # --- Owner ---

    def set_owner(self, owner):
        if owner:
            self.config_commands[
                'owner'] = "uci set gluon-node-info.@owner[0].contact='{0}' && uci commit gluon-node-info".format(owner)

    def get_owner(self):
        return self.config['gluon-node-info.@owner[0].contact']

    owner = property(fset=set_owner, fget=get_owner)

    # --- Longitude ---

    def set_longitude(self, longitude):
        if longitude:
            self.config_commands[
                'longitude'] = 'uci set gluon-node-info.@location[0].longitude={0} && uci commit gluon-node-info'.format(
                longitude)

    def get_longitude(self):
        return float(self.config['gluon-node-info.@location[0].longitude'])

    longitude = property(fset=set_longitude, fget=get_longitude)

    # --- Latitude ---

    def set_latitude(self, latitude):
        if latitude:
            self.config_commands[
                'latitude'] = 'uci set gluon-node-info.@location[0].latitude={0} && uci commit gluon-node-info'.format(
                latitude)

    def get_latitude(self):
        return float(self.config['gluon-node-info.@location[0].latitude'])

    latitude = property(fset=set_latitude, fget=get_latitude)

    # --- Height ---

    def set_height(self, height):
        if height:
            self.config_commands[
                'height'] = 'uci set gluon-node-info.@location[0].height={0} && uci commit gluon-node-info'.format(
                height)

    def get_height(self):
        return float(self.config['gluon-node-info.@location[0].height'])

    height = property(fset=set_height, fget=get_height)

    # --- Share location ---

    def set_share_location(self, share):
        param = 1 if share else 0
        self.config_commands[
            'share_location'] = 'uci set gluon-node-info.@location[0].share_location={0} && uci commit gluon-node-info'.format(
            param)

    def get_share_location(self):
        return int(self.config['gluon-node-info.@location[0].share_location']) == 1

    share_location = property(fset=set_share_location, fget=get_share_location)

    ###

    def get_preserve_24_channel(self):
        pass

    # tunneldigger.mesh_vpn.enabled = '1'

    #
    # autoupdater.settings.enabled = '1'
    # autoupdater.settings.branch = 'stable'

    # 2.4 GHz channel user limit
    # 5 GHz channel user limit

    # Mesh on LAN
    # Mesh on WAN
    # Firmware branch
    # Auto-update

    # Bandwidth limitation
    # Bandwidth limitation upstream
    # Bandwidth limitation downstream

    #
    # Extra functions that are not really part of a configuration
    #

    def reboot_node(self):
        self._run('reboot')

    def restart_vpn(self):
        # TODO: implement function
        pass

    def restart_WLAN(self):
        self._run('wifi')

    def update_firmware(self):
        # TODO: implement function
        pass

    def enable_config_mode(self):
        self._run("uci set gluon-setup-mode.@setup_mode[0].enabled='1' && uci commit gluon-setup-mode && reboot")

    def add_ssh_key(self):
        # TODO: implement function
        pass


class Crontab:
    pass

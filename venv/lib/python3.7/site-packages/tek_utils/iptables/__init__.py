import sys
import subprocess
from configparser import SafeConfigParser

from tek import logger, cli, TException

from tek_utils.iptables.model import (Command, Flush, Rule, Target, Policy,
                                      Match, Append, StateMatch, DNAT, Reject,
                                      MacMatch, DeleteChains)

input = 'INPUT'
forward = 'FORWARD'
output = 'OUTPUT'
post_r = 'POSTROUTING'
prerouting = 'PREROUTING'

accept = 'ACCEPT'
drop = 'DROP'
reject = 'REJECT'
masq = 'MASQUERADE'
dest_nat = 'DNAT'

switches = {
    'policy': 'P',
    'append': 'A',
    'flush': 'F',
    'jump': 'j'
}

iptabler_dir = '/etc/iptabler'

accept = 'ACCEPT'
drop = 'DROP'
reject = 'REJECT'
masq = 'MASQUERADE'
dest_nat = 'DNAT'

est_rel = 'ESTABLISHED,RELATED'
new = 'NEW'

localhost = '127.0.0.1'


class Iptables(object):

    def __init__(self):
        self.commands = []
        parser = SafeConfigParser()
        parser.read(iptabler_dir + '/iptabler.conf')

        udp = []
        tcp = []
        self.wan_interface = 'eth0'
        self.lan_interfaces = []
        self.hosts = dict()
        self.ports = dict()

        try:
            general = dict(parser.items('general'))
            if 'udp' in general:
                udp = general['udp'].split()
            if 'tcp' in general:
                tcp = general['tcp'].split()
            if 'wan' in general:
                self.wan_interface = general['wan']
            if 'lans' in general:
                self.lan_interfaces = general['lans'].split()
            self.local_ports = {
                'udp': udp,
                'tcp': tcp
            }
        except:
            logger.warn('no general section in config')
        for interface in self.lan_interfaces:
            self.hosts[interface] = dict()
            try:
                self.hosts[interface] = dict(parser.items('hosts_' +
                                                          interface))
            except:
                logger.warn('LAN \'%s\' defined, but no hosts section found!' %
                            interface)
        try:
            ports = dict(parser.items('ports'))
        except:
            logger.warn('No ports section in config')
        try:
            for hostprot in list(ports.keys()):
                host, protocol = hostprot.split('/')
                self.ports[hostprot] = [host, protocol,
                                        ports[hostprot].split()]
        except:
            logger.warn('Syntax error in portlist')

    def add_command(self, cmd):
        """ run iptables process with given args """
        assert(isinstance(cmd, Command))
        logger.info(cmd.string)
        self.commands.append(cmd)

    def __call__(self, *params):
        self.add_command(Append(*params))

    def launch(self):
        for command in self.commands:
            proc = subprocess.Popen(args=['iptables'] + command.strings,
                                    stderr=subprocess.PIPE)
            proc.wait()
            err = proc.stderr.readlines()
            if err:
                logger.error(''.join([l.decode() for l in err]))
                msg = 'Something went wrong. Most likely you are not root.'
                raise TException(msg)

    def flush(self, table=None):
        """ flush given table """
        self.add_command(Flush(table))

    def delete_chains(self):
        self.add_command(DeleteChains())

    def setup_local(self):
        for chain in [input, forward]:
            self.add_command(Policy(chain, drop))
        self.add_command(Policy(output, accept))
        self(input, Target(accept), Match("state", state=est_rel))
        self(input, Rule(source=localhost), Target(accept))

    def setup_lan_hosts(self):
        """ read the config files, extract host ip and mac adresses to enable
        ip forwarding filenames must begin with hosts_ and have the
        interface name as prefix
        """
        for interface in self.lan_interfaces:
            for hostip, hostmac in self.hosts[interface].items():
                self.setup_lan_host(interface, hostip, hostmac)

    def setup_lan_host(self, interface, hostip, hostmac):
        """ this currently allows:
            incoming connections from lan to be forwarded and locally
            incoming connections from wan to be forwarded, if they are
            ESTABLISHED or RELATED
        """
        from_host = Rule(inMinterface=interface, source=hostip)
        to_host = Rule(destination=hostip)
        est_rel = StateMatch('ESTABLISHED,RELATED')
        macmatch = MacMatch(hostmac)
        self(input, from_host, macmatch)
        self(forward, est_rel, to_host)
        self(forward, from_host, Rule(outMinterface=self.wan_interface),
             macmatch)
        self.enable_masquerading(hostip)

    def enable_masquerading(self, hostip=None):
        self('POSTROUTING', Rule(table='nat', source=hostip,
                                 outMinterface=self.wan_interface),
             Target('MASQUERADE'))

    def setup_ports(self):
        """ reads the ports to be opened from the conffile """
        for protocol, ports in self.local_ports.items():
            self.open_local_ports(protocol=protocol, portlist=ports)
        for (host, protocol, ports) in self.ports.values():
            self.forward_ports(protocol=protocol, portlist=ports,
                               destination=host)

    def open_local_ports(self, portlist, protocol='tcp'):
        """ open input ports """
        for port in portlist:
            self(input, Rule(protocol=protocol, dport=port), StateMatch(new))

    def forward_ports(self, portlist, destination, protocol='tcp'):
        """ forward given ports to host destination """
        for port in portlist:
            portrule = Rule(inMinterface=self.wan_interface, protocol=protocol,
                            dport=port)
            self(forward, portrule, StateMatch(new),
                 Rule(destination=destination))
            self(prerouting, Rule(table='nat'), portrule, DNAT(destination))

    def allopen(self):
        for chain in [input, forward, output]:
            self.add_command(Policy(chain, accept))
        self.enable_masquerading()

    def reject_remaining(self):
        for chain in [input, forward]:
            self(chain, Rule(protocol='tcp', inMinterface=self.wan_interface),
                 Reject('tcp-reset'))
            self(chain, Rule(protocol='udp', inMinterface=self.wan_interface),
                 Reject('icmp-port-unreachable'))


@cli
def iptabler():
    iptables = Iptables()
    iptables.flush()
    iptables.flush('nat')
    iptables.delete_chains()
    if len(sys.argv) > 1 and sys.argv[1] == "allopen":
        iptables.allopen()
    elif len(sys.argv) > 1 and sys.argv[1] == "minimal":
        iptables.setup_local()
    else:
        iptables.setup_local()
        iptables.setup_lan_hosts()
        iptables.setup_ports()
        iptables.launch()

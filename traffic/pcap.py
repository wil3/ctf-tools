import dpkt
from optparse import OptionParser
import netifaces
import netaddr
import socket
import urllib
import requests
import traceback

class TrafficAnalyzer:
    GEOIP_ENDPOINT = "http://ip-api.com/json"

    def __init__(self, pcap, interface="eth0"):
        self.interface = interface
        self.iptogeo = {}
        self.pcap = pcap
                


    def open(self, pcap_file):
        self.f = open(pcap_file)
        self.pcap = dpkt.pcap.Reader(f)

    def close(self):
        self.f.close()

    def process(self):
        self._process()

    def _is_syn(self, flags):
        syn_flag = ( flags & dpkt.tcp.TH_SYN ) != 0
        ack_flag = ( flags & dpkt.tcp.TH_ACK ) != 0
        return syn_flag and not ack_flag 

    def _get_default_gateway(self):
        gws = netifaces.gateways()
        gateway = gws['default'][netifaces.AF_INET][0]
        return gateway

    def _get_default_iface(self):
        gws = netifaces.gateways()
        iface = gws['default'][netifaces.AF_INET][1]
        return iface
    
    def _get_network(ip, subnet):
        ipsubnet = "{}/{}".format(ip,subnet)
        net = netaddr.IPNetwork(ipsubnet)
        return net.network

    def _get_addr(self, iface):
        addrs = netifaces.ifaddresses(iface)
        return addrs[netifaces.AF_NET]

    def get_geolocation_for_ip(self, ip):
        url = '{}/{}'.format(self.GEOIP_ENDPOINT, ip)
        res = requests.get(url)
        return res.json()

    def get_external_ips(self): 
        pass

    def get_origin_network(self):
        """ Look at all the ips and make a best guess what the 
        network prefix is. Basically this is a k=2 cluster.
        """ 
        pass

    def get_external_ips2(self):
        ips = []

        for ts, pkt in self.pcap:
            try:
                eth = dpkt.ethernet.Ethernet(pkt)
                ip = eth.data
                ip.src
            except:
                pass

    def _decode_dns(self, rr):
        r_type = rr.type
        r_data = rr.rdata
        print rr.name
        if r_type == dpkt.dns.DNS_A  :
           print socket.inet_ntoa( r_data )
        elif r_type == dpkt.dns.DNS_AAAA :
           print  socket.inet_ntop( socket.AF_INET6, r_data )

    def _whitelisted(self, query):
        whitelist = ['msftncsi.com', 'microsoft.com', 'windows.com']
        for q in query:
            for domain in whitelist:
                if q.name in domain:
                    return True
        return False

    def failed_dns(self):
        nxdomain = 0
        valid = 0
        with open(self.pcap, 'rb') as f:
            self.pcap = dpkt.pcap.Reader(f)
            #self.pcap.setfilter('udp dst port 53')
            for ts, pkt in self.pcap:
                try:
                    eth = dpkt.ethernet.Ethernet(pkt)
                    ip = eth.data
                    """
                    if len(udp) > 0:
                        print udp
                        dns = dpkt.dns.DNS(udp.data)
                        print dns
                    """
                    if type(ip.data) is dpkt.udp.UDP:
                        udp = ip.data
                        #we just want responses
                        if udp.sport == 53 : 
                            dns = dpkt.dns.DNS(udp.data)
                            


                            if dns.qr == dpkt.dns.DNS_R:
                                #What is being quiered?
                                if self._whitelisted(dns.qd):
                                    continue

                                print dns.qd[0].name
                                #for qd in dns.qd:
                                #    pass
                                    #print qd.name
                                if dns.rcode  == dpkt.dns.DNS_RCODE_NOERR :
                                    valid = valid + 1
                                    for rr in dns.an:
                                        self._decode_dns(rr)
                                elif dns.rcode == dpkt.dns.DNS_RCODE_NXDOMAIN :
                                    print "NXDOMAIN"
                                    nxdomain = nxdomain + 1

                                #print dns.qr
                                #print dns.aa
                                #print dns.ar
                                #print dir(dns)
#print dir(udp)
                            #print ""
                    if type(ip.data) is dpkt.tcp.TCP:
                        http = dpkt.http.Response(ip.data.data)
                        if http.status == 404: 
                            pass

                except:
                    traceback.print_exc()

        return (valid, nxdomain)

    def _process(self):
        for ts, pkt in self.pcap:
            try:
                eth = dpkt.ethernet.Ethernet(pkt)
                ip = eth.data
                if type(ip.data) is dpkt.tcp.TCP:
                    tcp = ip.data
                    # Just in case no filter on capture, only are interested in 
                    # inital connection and external sources
                    if self._is_syn(tcp.flags):
                        pass

            except:
                pass

if __name__ == "__main__":
    usage = "usage: %prog [options] FILE"
    parser = OptionParser(usage=usage) 
    (options, args) = parser.parse_args()
    pcap = args[0]
    traffic = TrafficAnalyzer(pcap)
    traffic.failed_dns()
    #traffic.open(pcap)
    #traffic.process()
    #traffic.get_location()
    #traffic.close()

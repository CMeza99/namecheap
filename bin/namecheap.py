#!/root/namecheap/bin/python

import logging
import socket
#from xml.dom import minidom

import requests
import fire
import sys
print(sys.version_info)

FORMAT = '%(asctime)-15s  %(message)s'
logging.basicConfig(format=FORMAT)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

class UpdateDNS():
    def __init__(self, host, domain, password, ip=None, find_ip=False):
        _LOGGER.debug('--- init ---')
        self.host = host
        self.domain = domain
        self.__password = password
        self.ip = ip
        self.find_ip = find_ip
        self.result = None

        if find_ip:
            self.ip = self._host_ip

        #if (not self.ip) or self._current_ip != self.ip:
        #    self.result = self.update_record()

        self.update_record()

    def __str__(self):
        return self.result.text

#    @property
#    def _current_ip(self):
#        _LOGGER.debug('DNS lookup for %s', '{}.{}'.format(self.host,self.domain))
#        ip = None
#
#        try:
#            ip = socket.gethostbyname('{}.{}'.format(self.host,self.domain))
#        except socket.gaierror:
#            _LOGGER.critical('Lookup failed. Record my not exist')
#        else:
#            _LOGGER.debug('Resolving to %s', ip)
#            raise
#
#        return ip

    @property
    def _host_ip(self):
        _LOGGER.debug('Looking up default ip on host')
        ip = None
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
        _LOGGER.debug('Default IP: %s', ip)
        return ip
    
    def update_record(self):
        url = 'https://dynamicdns.park-your-domain.com/update'
        params = {
                'host': self.host,
                'domain': self.domain,
                'password': self.__password
                }
        if self.ip: params.update({'ip': self.ip})

        _LOGGER.debug('Attempting to update %s.%s', self.host, self.domain)
        self.result = requests.get(url, params=params, verify=True)
        _LOGGER.debug('Response status code: %s', self.result.status_code)
        self.result.raise_for_status()

        # Need to figure out how to parse return better
        #xmldoc = minidom.parseString(self.result.text)
        #_LOGGER.info('Response text: %s', xmldoc.getElementsByTagName('ResponseString')[0].firstChild.nodeValue)
        return self.result


if __name__ == "__main__":
    fire.Fire(UpdateDNS)

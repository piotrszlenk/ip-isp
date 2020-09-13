import registry.objects
import pprint
import ipaddress
import pymongo

class DB:
  def __init__(self):
    self.ip_dict = {}
    self.mongo_client = pymongo.MongoClient('mongodb://localhost:27017')
    self.mongo_db = self.mongo_client['ip2asn']

  def add_ip(self, ip):
    ip = self.mongo_db.ips.find_one({'addr': ip.addr})
    if not ip:
      self.mongo_db.ips.insert_one({'addr': ip.addr})
    return ip

  def get_ip(self, addr):
    return self.mongo.ips.find_one({'addr': addr})

  def del_ip(self, addr):
    self.ip_dict.pop(addr, None)

  def update_ip(self, ip, asn, cidr):
    if str(ip.addr) in self.ip_dict:
      ip = self.ip_dict[str(ip.addr)]
      if not(ip.asn or ip.cidr):
        ip.asn = asn
        ip.cidr = cidr
        return ip
      else:
        return ip
    else:
      raise Exception("IP %d does not exist in IP db, so cannot update it.", str(ip.addr))    

  def add_asn(self, num, desc, cc):
    if num not in self.asn_dict:
      asn = registry.objects.ASN(num, desc, cc)
      self.asn_dict[num] = asn
      return asn
    return self.asn_dict[num]

  def add_cidr(self, asn_num, cidr_net):
    if asn_num in self.asn_dict:
      asn = self.asn_dict[asn_num]
      if cidr_net not in self.cidr_dict: 
        cidr = registry.objects.CIDR(asn, cidr_net)
        asn.add_cidr(cidr)
        self.cidr_dict[cidr_net] = cidr
        return cidr
      return self.cidr_dict[cidr_net]
    else:
      raise Exception("ASN %d does not exist in ASN db, so cannot add CIDR.", asn_num)

  def db_dump(self):
    for ip in self.ip_dict:
      pprint.pprint(str(self.ip_dict[ip].addr)+";"+str(self.ip_dict[ip].asn.num)+";"+str(self.ip_dict[ip].asn.desc)+";")

  def find_cidr_match(self, addr):
    # improve to find the best match, not the first match
    for cidr_addr in self.cidr_dict.keys():
      if ipaddress.ip_address(addr) in ipaddress.ip_network(cidr_addr):
        return self.cidr_dict[cidr_addr]
    return None
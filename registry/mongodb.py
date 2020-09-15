import registry.objects
import pprint
import ipaddress
import pymongo
from pymongo import ReturnDocument 

class DB:
  def __init__(self):
    self.ip_dict = {}
    self.mongo_client = pymongo.MongoClient('mongodb://localhost:27017')
    self.mongo_db = self.mongo_client['ip2asn']

  def add_ip(self, ip):
    # Return IP object if found or create a new one
    return self.mongo_db.ips.find_one_and_update({'addr': ip.addr }, {'$set': {'addr': ip.addr} }, upsert=True, return_document=ReturnDocument.AFTER)

  def add_asn(self, asn):
    # Return ASN object if found or create a new one
    return self.mongo_db.asns.find_one_and_update({'num': asn.num }, {'$set': {'num': asn.num} }, upsert=True, return_document=ReturnDocument.AFTER)

  def add_cidr(self, cidr):
    # Return CIDR object if found or create a new one
    return self.mongo_db.cidrs.find_one_and_update({'addr': cidr.addr}, {'$set': {'addr': cidr.addr} }, upsert=True, return_document=ReturnDocument.AFTER)

  def get_ip(self, addr):
    return self.mongo_db.ips.find_one({'addr': addr})

  def add_asn_to_ip(self, ip, asn):
    return self.mongo_db.ips.find_one_and_update({'_id' : ip['_id']}, {'$set': {'asn_id': asn['_id']} }, upsert=True, return_document=ReturnDocument.AFTER)

  def add_asn_to_cidr(self, cidr, asn):
    return self.mongo_db.cidrs.find_one_and_update({'_id': cidr['_id']}, {'$set': {'asn_id': asn['_id']} }, upsert=True, return_document=ReturnDocument.AFTER)

  def find_cidr_match(self, addr):
    # improve to find the best match, not the first match
    for cidr in self.mongo_db.cidrs.find():
      if ipaddress.ip_address(addr) in ipaddress.ip_network(cidr['addr']):
        return cidr
    return None


#    if str(ip.addr) in self.ip_dict:
#      ip = self.ip_dict[str(ip.addr)]
#      if not(ip.asn or ip.cidr):
#        ip.asn = asn
#        ip.cidr = cidr
#        return ip
#      else:
#        return ip
#    else:
#      raise Exception("IP %d does not exist in IP db, so cannot update it.", str(ip.addr))    



#  def add_cidr(self, asn_num, cidr_net):
#    if asn_num in self.asn_dict:
#      asn = self.asn_dict[asn_num]
#      if cidr_net not in self.cidr_dict: 
#        cidr = registry.objects.CIDR(asn, cidr_net)
#        asn.add_cidr(cidr)
#        self.cidr_dict[cidr_net] = cidr
#        return cidr
#      return self.cidr_dict[cidr_net]
#    else:
#      raise Exception("ASN %d does not exist in ASN db, so cannot add CIDR.", asn_num)

  def ip_dump(self):
    for ip in self.mongo_db.ips.find():
      print(ip)

  def asn_dump(self):
    for asn in self.mongo_db.asns.find():
      print(asn)

  def cidr_dump(self):
    for cidr in self.mongo_db.cidrs.find():
      print(cidr)



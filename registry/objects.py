import ipaddress

class IP:
  def __init__(self, addr):
    self.addr = ipaddress.ip_address(addr)
    self.asn = None
    self.cidr = None

class ASN:
  def __init__(self, num, desc, cc):
    self.num = num
    self.cidrs = {}
    self.desc = desc
    self.cc = cc

  def add_cidr(self, cidr):
    if str(cidr.addr) not in self.cidrs:
      self.cidrs[str(cidr.addr)] = cidr
    return self.cidrs[str(cidr.addr)]

class CIDR:
  def __init__(self, asn, addr):
    self.addr = ipaddress.ip_network(addr)
    self.asn = asn
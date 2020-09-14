import ipaddress

class IP:
  def __init__(self, addr):
    self.addr = addr
    self.asn = None
    self.cidr = None

class ASN:
  def __init__(self, num, desc, cc):
    self.num = num
    self.desc = desc
    self.cc = cc

  def add_cidr(self, cidr):
    if str(cidr.addr) not in self.cidrs:
      self.cidrs[str(cidr.addr)] = cidr
    return self.cidrs[str(cidr.addr)]

class CIDR:
  def __init__(self, addr):
    self.addr = addr
    self.asn = None
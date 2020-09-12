import ipaddresses

class IP:
  def __init__(self, addr):
    self.addr = addr
    self.asn = None
    self.cidr = None

class ASN:
  def __init__(self, num, desc, cc):
    self.num = num
    self.cidrs = {}
    self.desc = desc
    self.cc = cc

  def add_cidr(self, cidr):
    if cidr.cidr_addr not in self.cidrs:
      self.cidrs[cidr.cidr_addr] = cidr

class CIDR:
  def __init__(self, asn, cidr_addr):
    self.cidr_addr = cidr_addr
    self.asn = asn
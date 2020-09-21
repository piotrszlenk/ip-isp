import threading

class IPLookupThread(threading.Thread):
  def __init__(self, db, queue, event):
    threading.Thread.__init__(self)
    self.db = db
    self.queue = queue
    self.event = event

  def run(self):
    print("Starting thread {}".format(threading.current_thread().ident))
    while not self.event.is_set() or not self.queue.empty():
      ip_addr = self.queue.get()
      cidr = self.db.find_cidr_match(ip_addr)
      if cidr:
        print('Found matching CIDR in the DB for {}. CIDR: {} '.format(ip_addr, cidr))
        #
        #self.db.update_ip(self.db.add_ip(str(ip)), cidr.asn, cidr)
      else:
        try:
          print("Thread {} is processing {}".format(threading.current_thread().ident,ip_addr))
          r = ipwhois.IPWhois(ip_addr).lookup_rdap(asn_methods=['whois', 'http'])
          ip = self.db.add_ip(registry.objects.IP(ip_addr))
          if r['asn'] is not None and r['asn_cidr'] is not None and r['asn'] != "NA" and r['asn_cidr'] != "NA":
            asn = self.db.add_asn(registry.objects.ASN(r['asn'], r['asn_description'], r['asn_country_code']))
            cidr = self.db.add_cidr(registry.objects.CIDR(r['asn_cidr']))
            self.db.add_asn_to_cidr(cidr, asn)
            self.db.add_asn_to_ip(ip, asn)
        except ipwhois.exceptions.IPDefinedError as e:
          print('Cannot lookup following IP: {}. {}'.format(str(ip_addr), e))
          continue
        except ipwhois.exceptions.ASNRegistryError as e:
          print('Failed during lookup of IP: {}. {}'.format(str(ip_addr), e))
          continue        
        except ipwhois.exceptions.HTTPLookupError as e:
          print('Failed during lookup of IP: {}. {}'.format(str(ip_addr), e))
          continue        
      self.queue.task_done()
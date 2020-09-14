import ipwhois
import pprint
import registry.objects
import registry.mongodb
import ipaddress
import argparse
import threading
import queue

def main():
  parser = argparse.ArgumentParser(description='Perform ASN lookup based on IP address.')
  parser.add_argument("ip_file", help="Flat text file with IP addresses", type=str)
  parser.add_argument("output_file", help="Flat text file with IP addresses", type=str)
  args = parser.parse_args()

  db = registry.mongodb.DB()
  #ip_list = []

  #Threading
  threads = []
  db_lock = threading.Lock()
  ip_queue = queue.Queue()  
  terminate_event = threading.Event()

  for i in range(4):
    t = IPLookupThread(db, ip_queue, terminate_event)
    threads.append(t)
    t.start()

  # Fill the queue
  with open(args.ip_file, 'r') as infile:
    for line in infile:
      try:
        l = line.strip()
        if ipaddress.ip_address(l):
          ip_queue.put(l) 
      except Exception as e:
        print('Unable to parse line {} as IP. Skipping.'.format(l, e))

  terminate_event.set()
  for t in threads:
    t.join()

  db.ip_dump()
  db.asn_dump()
  db.cidr_dump()

#  with open(args.output_file, 'w') as outfile:
#    for ip in db.ip_dict:
#      out_ip = str(db.ip_dict[ip].addr)
#      out_asn = db.ip_dict[ip].asn.num if db.ip_dict[ip].asn is not None else ""
#      out_asn_desc = db.ip_dict[ip].asn.desc if db.ip_dict[ip].asn is not None else ""
#      outfile.write(out_ip+";"+out_asn+";"+out_asn_desc+"\n")


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


#      cidr = self.db.find_cidr_match(str(ip))
#      if cidr:
#        print('Found matching CIDR in the DB for: {}'.format(str(ip)))
#        self.db.update_ip(self.db.add_ip(str(ip)), cidr.asn, cidr)      
#      else:
#        try:
#          r = ipwhois.IPWhois(str(ip)).lookup_rdap(asn_methods=['whois', 'http'])
#          ip = self.db.add_ip(str(ip))
#          if r['asn'] is not None and r['asn_cidr'] is not None and r['asn'] != "NA" and r['asn_cidr'] != "NA":
#            #pprint.pprint(r)
#            asn = self.db.add_asn(r['asn'], r['asn_description'], r['asn_country_code'])
#            cidr = self.db.add_cidr(r['asn'], r['asn_cidr'])
#            self.db.update_ip(ip, asn, cidr)
#        except ipwhois.exceptions.IPDefinedError as e:
#          print('Cannot lookup following IP: {}. {}'.format(str(ip), e))
#          continue
#        except ipwhois.exceptions.ASNRegistryError as e:
#          print('Failed during lookup of IP: {}. {}'.format(str(ip), e))
#          continue
#      

if __name__ == "__main__":
  main()
import ipwhois
import pprint
import registry.objects
import registry.db
import ipaddress

def main():
  db = registry.db.DB()
  with open('ips.txt', 'r') as infile:
    for line in infile:
      l = line.strip()
      db.add_ip(ipaddress.ip_address(l))

#  for ip in db.ip_dict:
#    r = ipwhois.IPWhois(db.ip_dict[ip].addr).lookup_rdap(depth=1)
#    asn = db.add_asn(r['asn'], r['asn_description'], r['asn_country_code'])
#    cidr = db.add_cidr(r['asn'], r['asn_cidr'])
#    db.update_ip(db.ip_dict[ip], asn, cidr)

#  db.db_dump()
  
if __name__ == "__main__":
  main()
import ipwhois
import pprint
import registry.objects
import registry.db
import ipaddress

def main():
  db = registry.db.DB()
  ip_list = []
  
  with open('ips_limited.txt', 'r') as infile:
    for line in infile:
      try:
        l = line.strip()
        ip_list.append(ipaddress.ip_address(l))
      except Exception as e:
        print('Unable to parse line {} as IP. Skipping.'.format(l, e))
        continue

  for ip in ip_list:
    print('Processing IP: {}'.format(str(ip)))
    # Check existing CIDRs for potential matches otherwise perform lookup
    cidr = db.find_cidr_match(str(ip))
    if cidr:
      print('Found matching CIDR in the DB for: {}'.format(str(ip)))
      db.update_ip(db.add_ip(str(ip)), cidr.asn, cidr)      
    else:
      try:
        r = ipwhois.IPWhois(str(ip)).lookup_rdap(depth=1)    
        ip = db.add_ip(str(ip))
        asn = db.add_asn(r['asn'], r['asn_description'], r['asn_country_code'])
        cidr = db.add_cidr(r['asn'], r['asn_cidr'])
        db.update_ip(ip, asn, cidr)
      except ipwhois.exceptions.IPDefinedError as e:
        continue

  with open('output.txt', 'w') as outfile:
    for ip in db.ip_dict:
      outfile.write(str(db.ip_dict[ip].addr)+";"+str(db.ip_dict[ip].asn.num)+";"+str(db.ip_dict[ip].asn.desc)+";\n")
  
if __name__ == "__main__":
  main()
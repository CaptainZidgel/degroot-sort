import json
import sys
import ipaddress

def unfurl_relays(src="NetworkDatagramConfig.json", psep=":"):
	try:
		l = []
		with open(src, "r") as f: 
			servers = json.loads(f.read())
			for pop in servers['pops']:
				key, pop = pop, servers['pops'][pop]
				try:
					relays = pop['relays']
				except KeyError:
					#print("No relay:", key)
					pass
				try:
					ranges = pop['service_address_ranges']
				except KeyError:
					#print("No range:", key)
					pass
				if 'relays' in pop:
					for r in relays:
						for p in range(r["port_range"][0], r["port_range"][1]+1):
							ip = r['ipv4']+psep+str(p)
							l.append(ip)
				
				if 'service_address_ranges' in pop:
					if "-" in ranges[0]:
						ran = ranges[0].split("-")
						lx = [ip for ip in ipaddress.summarize_address_range(ipaddress.IPv4Address(ran[0]), ipaddress.IPv4Address(ran[1]))]
						for r in lx: #https://gist.github.com/vndmtrx/dc412e4d8481053ddef85c678f3323a6#gistcomment-3294226
							net = ipaddress.ip_network(r)
							for host in net.hosts():
								l.append(str(host))
					else:
						for r in ranges: #https://gist.github.com/vndmtrx/dc412e4d8481053ddef85c678f3323a6#gistcomment-3294226
							net = ipaddress.ip_network(r)
							for host in net.hosts():
								l.append(str(host))

			#json.dump(l, FILE_TO_SAVE_TO)
		return set(l)
	except FileNotFoundError:
		print("No list of Valve servers found.")
		return set()


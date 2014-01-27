 #!/usr/bin/python

import requests
import HTMLParser
import datetime
import argparse

def ts():
	return str(datetime.datetime.now())

class ParseMiddleCoin(HTMLParser.HTMLParser):
	addr_data_keys = {6:"id",
				 5:"accepted_hr",
				 4:"rejected_hr",
				 3:"imm_unexch_bal",
				 2:"unexch_bal",
				 1:"bal",
				 0:"ignore"}

	def __init__(self, lookfor):
        # initialize the base class
		HTMLParser.HTMLParser.__init__(self)
		self.save_tags = 0
		self.addr_data = {}
		self.addr = {}
		self.lookfor = lookfor

	def handle_starttag(self, tag, attrs):
		if tag == "td":
			for attr in attrs:
				if(attr[0] == 'id'):
					if attr[1] in lookfor:
						self.addr_data = {}
						self.save_tags = 6

	def handle_data(self, local_data):
			if self.save_tags > 0:
				addr_data_key = ParseMiddleCoin.addr_data_keys[self.save_tags]
				self.addr_data[addr_data_key] = local_data

	def handle_endtag(self, tag):
		if self.save_tags > 0:
			self.save_tags -= 1

			if self.save_tags == 0:
				for key in self.addr_data:
					if self.addr_data[key] == '\n':
						self.addr_data[key] = None				

				if self.addr_data["imm_unexch_bal"] is not None:
					self.addr_data["imm_unexch_bal"] = \
						float(self.addr_data["imm_unexch_bal"])
				else:
					self.addr_data["imm_unexch_bal"] = 0

				if self.addr_data["unexch_bal"] is not None:
					self.addr_data["unexch_bal"] = \
						float(self.addr_data["unexch_bal"])
				else:
					self.addr_data["unexch_bal"] = 0

				if self.addr_data["bal"] is not None:
					self.addr_data["bal"] = \
						float(self.addr_data["bal"])
				else:
					self.addr_data["bal"] = 0

				self.addr_data["btc_total"] = self.addr_data["bal"] + \
											self.addr_data["unexch_bal"] + \
											self.addr_data["imm_unexch_bal"]

				addr_id = self.addr_data["id"]
				self.addr[addr_id] = self.addr_data

if __name__ == "__main__":
	argparser = argparse.ArgumentParser(
									description='Check on middlecoin stats')

	argparser.add_argument('addresses', metavar='"address,address,address"', 
		type=str, nargs='+',help='addresses to look for')

	args = argparser.parse_args()
	lookfor = {}
	for address in args.addresses[0].split(','):
		lookfor[address.strip()] = True

	print "[+] [%s] Requesting middlecoin data" % (ts())
	r = requests.get('http://middlecoin.com/allusers.html')
	text = r.text
	print "[+] [%s] Got middlecoin data: %d bytes" % (ts(), len(text))

	print "[+] [%s] Parsing Text" % (ts())
	parser = ParseMiddleCoin(lookfor)
	parser.feed(text)

	print "[+] [%s] Printing CSV" % (ts())

	print "Datetime,Address,BTC Total"
	btc_totals = []
	for address in parser.addr:
		print "%s, %s,%s, [%s]" % (ts(), address, 
									parser.addr[address]["btc_total"], 
									parser.addr[address])
		
		btc_totals.append(parser.addr[address]["btc_total"])

	print "[+] [%s] Bitcoin Total: %s" % (ts(), sum(btc_totals))

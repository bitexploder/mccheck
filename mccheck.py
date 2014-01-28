import requests
import json
import datetime
import argparse

def ts():
    return str(datetime.datetime.now())

class ParseMiddleCoin(object):
    def __init__(self, json_bytes, lookfor):
        self.save_tags = 0
        self.addr_data = {}
        self.addr = {}
        self.lookfor = lookfor
        self.json_bytes = json_bytes

        self.json_bytes = json.loads(self.json_bytes)

    def process_reports(self):
        for address in self.lookfor:
            for report in parser.json_bytes['report']:
                if address == report[0]:
                    self.addr[address] = {}
                    report_data = report[1]

                    if 'unexchangedBalance' in report_data:
                        self.addr[address]['unexch_bal'] = \
                            float(report_data['unexchangedBalance'])
                    else:
                        self.addr[address]['unexch_bal'] = 0.0

                    if 'bitcoinBalance' in report_data:
                        self.addr[address]['bal'] = \
                            float(report_data['bitcoinBalance'])
                    else:
                        self.addr[address]['bal'] = 0.0

                    if 'immatureBalance' in report_data:                   
                        self.addr[address]['imm_unexch_bal'] = \
                            float(report_data['immatureBalance'])
                    else:
                        self.addr[address]['imm_unexch_bal'] = 0.0

                    self.addr[address]['btc_total'] = \
                        self.addr[address]['unexch_bal'] + \
                        self.addr[address]['bal'] + \
                        self.addr[address]['imm_unexch_bal']

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Check on middlecoin stats')
    argparser.add_argument('addresses', metavar='"address,address,address"', type=str, nargs='+',
                       help='addresses to look for')

    args = argparser.parse_args()
    lookfor = {}
    for address in args.addresses[0].split(','):
        lookfor[address.strip()] = True

    print "[+] [%s] Requesting middlecoin data" % (ts())
    r = requests.get('http://middlecoin.com/json')
    text = r.text

    print "[+] [%s] Got middlecoin data: %d bytes" % (ts(), len(text))
    print "[+] [%s] Parsing Text" % (ts())

    parser = ParseMiddleCoin(text, lookfor)
    parser.process_reports()

    print "[+] [%s] Printing CSV" % (ts())
    print "Datetime,Address,BTC Total"
    
    btc_totals = []
    for address in parser.addr:
        print "%s, %s,%s, [%s]" % (ts(), address, 
                                    parser.addr[address]["btc_total"], 
                                    parser.addr[address])
        
        btc_totals.append(parser.addr[address]["btc_total"])

    print "[+] [%s] Bitcoin Total: %s" % (ts(), sum(btc_totals))

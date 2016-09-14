# coding: utf-8

import argparse
import time
import socket
import dns.resolver

def ip_or_hostname(argument):
    """ receives an ip or hostname, returns ip or raises ValueError """
    try:
        return socket.gethostbyname(argument)
    except socket.gaierror as e:
        raise ValueError(str(e))

# Parse command line args
parser = argparse.ArgumentParser(description='Test leg.br nameserver.')
parser.add_argument("NAMESERVER", type=ip_or_hostname,
        help = 'IP address or hostname of server to test.')
parser.add_argument('--tcp', action='store_true',
        help = 'Use TCP instead of UDP')
parser.add_argument('--timeout', action='store', type=float, default=5.0,
        help = 'Timeout for DNS queries in seconds. Default to 5.0s')
parser.add_argument('--verbose', action='store_true',
        help = 'Verbose output.')
args = parser.parse_args()

UFS=['ac', 'al', 'ap', 'am', 'ba', 'ce', 'df', 'es', 'go', 'ma', 'mt',
        'ms', 'mg', 'pa', 'pb', 'pr', 'pe', 'pi', 'rj', 'rn', 'rs',
        'ro', 'rr', 'sc', 'sp', 'se', 'to']
DOMAINS=['infra.leg.br']
for uf in UFS:
    DOMAINS.append(uf+'.leg.br')

# dns resolver setup
resolver = dns.resolver.Resolver()
resolver.nameservers = [str(args.NAMESERVER)]
resolver.lifetime = args.timeout
resolver.search = []

def logi(message):
    """ log information """
    if args.verbose:
        print(message)

logi('Testing %i domains: ' % len(DOMAINS))
failed_domains=[]
ok_domains=[]
start_time = time.time()
for domain in DOMAINS:
    try:
        answer = resolver.query(domain, 'SOA', tcp=args.tcp)
    except Exception as e:
        print('E', end='', flush=True)
        failed_domains.append((domain, e))
        continue
    print('.', end='', flush=True)
    soa=answer[0]
    ok_domains.append((domain, soa))
end_time = time.time()
print('')

# test results
for domain, soa in ok_domains:
    logi("OK %s, %s" % (domain, soa))
for domain, exception in failed_domains:
    print("ERR", domain, type(exception), str(exception), sep=', ')
logi("Elapsed time: %0.3f seconds" % (end_time - start_time))


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
        help = 'IP address or hostname of nameserver to test.')
parser.add_argument("DOMAIN", type=str,
        help = 'Domain to ask SOA record for.')
parser.add_argument('--tcp', action='store_true',
        help = 'Use TCP instead of UDP')
parser.add_argument('--timeout', action='store', type=float, default=2.9,
        help = 'Timeout for DNS queries in seconds. Default to 2.9s')
parser.add_argument('--verbose', action='store_true',
        help = 'Verbose output.')
args = parser.parse_args()

# dns resolver setup
resolver = dns.resolver.Resolver()
resolver.nameservers = [str(args.NAMESERVER)]
resolver.lifetime = args.timeout
resolver.search = []

def logi(message):
    """ log information """
    if args.verbose:
        print(message)

logi('Testing domain %s on nameserver %s' % (args.DOMAIN, args.NAMESERVER))
start_time = time.time()
try:
    answer = resolver.query(args.DOMAIN, 'SOA', tcp=args.tcp)
    print("OK %s, IN SOA: %s" % (args.DOMAIN, answer[0]))
except Exception as e:
    print("ERR %s" % args.DOMAIN, type(e), str(e), sep=', ')
end_time = time.time()

logi("Elapsed time: %0.3f seconds" % (end_time - start_time))


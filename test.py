#!/usr/bin/python

import sys
import re
import IP

def find_address(ip):
    country = "unknown"
    proivnce = "unknown"
    city = "unknown"
    address = IP.find(ip)

    if address:
        details = address.split("\t")
        if len(details) > 0:
            country = details[0]
            if len(details) > 1:
                proivnce = details[1]
                if len(details) > 2:
                    city = details[2]

    return country,proivnce,city


country,proivnce,city = find_address('223.247.75.183')
print('%s %s %s' % (country,proivnce,city))

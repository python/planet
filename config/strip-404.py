#!/usr/bin/env python
import sys
import ConfigParser
import time
import urllib2
#
# Using requests because it handles things
# HTTPS better than urllib2 (at least on 2.7)
#
import requests

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'config.ini'
    
oconfig = ConfigParser.RawConfigParser()
oconfig.read(filename)

def write_section(f, section_name, prefix="", notes=""):
    f.write("%s[%s]\n" % (prefix, section_name))
    for key, value in oconfig.items(section_name):
        if "'" in key: key = '"%s"' % key
        f.write("%s%s = %s\n" % (prefix, key, str(value).replace('\n', '\n\t')))
    if notes:
        f.write("%snotes = %s\n" % (prefix, notes))
    f.write("%slast_checked = %s\n" % (prefix, time.asctime()))
    f.write("\n")

#
# This is basically a clone of sort-ini which leaves the sort
# order the same but checks whether a feed is giving an error
# and comments it out
#
with open(filename, "wb") as f:
    for section_name in oconfig.sections():
        print section_name
        if section_name == 'Planet':
            write_section(f, section_name)
        else:
            try:
                requests.get(section_name).raise_for_status()
            except requests.RequestException as exc:
                print "Failed because:", exc.message
                write_section(f, section_name, "# ", exc.message)
            except Exception as exc:
                print "Problem:", exc
                write_section(f, section_name, "# ")
            else:
                write_section(f, section_name)

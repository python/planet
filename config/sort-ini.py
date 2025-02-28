#!/usr/bin/env python

import sys
import configparser as ConfigParser

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "config.ini"

oconfig = ConfigParser.RawConfigParser()
oconfig.read(filename)

# This part will destroy the configuration if there's a crash while
# writing the output.  We're in an GIT-controlled directory, so
# I didn't care enough to fix this.
with open(filename, "wb") as fd:
    # Copy of write() code that sorts output by section
    if oconfig._defaults:
        fd.write("[%s]\n" % DEFAULTSECT)
        for key, value in oconfig._defaults.items():
            fd.write("%s = %s\n" % (key, str(value).replace("\n", "\n\t")))
        fd.write("\n")

    result = {}
    for section in sorted(oconfig._sections):
        if section == "Planet":
            fd.write(b"[%s]\n" % section.encode("utf-8"))
        for key, value in oconfig._sections[section].items():
            if key != "__name__":
                if section == "Planet":
                    fd.write(
                        b"%s = %s\n"
                        % (
                            key.encode("utf-8"),
                            str(value).replace("\n", "\n\t").encode("utf-8"),
                        )
                    )
                else:
                    result[value.replace('"', "")] = section
        if section == "Planet":
            fd.write("\n".encode("utf-8"))

    for key, value in sorted(result.items()):
        fd.write(b"[%s]\n" % value.encode("utf-8"))
        name = key
        if "'" in key:
            name = '"%s"' % key
        fd.write(b"name = %s\n" % name.encode("utf-8"))
        fd.write(b"\n")

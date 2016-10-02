#! /usr/bin/env python
from yapsy.IPlugin import IPlugin

import socket
import json
import os

import logging
logger = logging.getLogger("IExampleExporterPlugin")

varsFile = os.path.abspath(
    os.path.join(
        os.path.dirname(
            __file__),
        "..",
        "variables.tf.json"
    )
)


class IExampleExportPlugin(IPlugin):
    def collect_data(self):
        """Place some form of external data as json into a variables file"""

        addr_list = list()
        addrinfoList = socket.getaddrinfo(
            "example.com", 80, 0, 0, socket.IPPROTO_TCP)
        for lentry in addrinfoList:
            addr = lentry[4][0]
            print addr
            addr_list.append(addr)

        jsondata = {
            "variable": {
                "example_addresses": {
                    "description": "example.com address entries",
                    "default": addr_list,
                }
            }
        }

        with open(varsFile, "w") as jsonfile:
            json.dump(jsondata, jsonfile, sort_keys=True, indent=2)

        logger.info("Wrote %d addresses to %s", len(addr_list), varsFile)
        return len(addr_list)


if __name__ == "__main__":
    import sys
    sys.exit(IExampleExportPlugin().collect_data())

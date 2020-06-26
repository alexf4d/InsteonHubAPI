import requests
import base64
from lxml import objectify, etree

from typing import List
import re


class ISY():
    authorization = ""
    ip = ""
    nodes = {}
    def __init__(self, username, password, ip):
        self.authorization = (username, password)
        self.ip = ip
    
    def get_nodes(self, method):
        """
        Gets available nodes from the hub.

        :param method: pass "name" for name referenced or "address" for address referenced
        :returns: Null
        """

        extension = "/rest/nodes"
        response = Messenger.get(extension, self.authorization, self.ip)
        xml = response.text.encode('utf8')
        root = objectify.fromstring(xml)

        self.nodes = {}
        for node in root.iterchildren(tag='node'):
            if method == "name":
                name = str(node.name)
            elif method == "address":
                name = str(node.address)
            else:
                return

            # just passed a reference to THIS instance (using self as last argument to Node constructor)
            self.nodes[node.name] = Node(node.name, node.address, node.type, "unknown", node.property.get("uom"), self)

class Node():

    def __init__(self, name, address, category, status, properties, parent):
        # feel free to rename
        self.parent = parent
        
        self.name = name
        self.address = address
        self.category = category
        self.status = status
        self.properties = {
            'Dimmer':False,
            'On':False,
            'Off':False,
            'Low':False,
            'Medium':False,
            'High':False
            }
        if "%" in properties:
            self.properties["Dimmer"] = True
        if "on" in properties:
            self.properties["On"] = True
        if "off" in properties:
            self.properties["Off"] = True
        if "low" in properties:
            self.properties["Low"] = True
        if "med" in properties:
            self.properties["Medium"] = True
        if "high" in properties:
            self.properties["High"] = True

    def __str__(self):
        return str(self.name)
    
    def on(self):
        extension = "/rest/nodes/{}/cmd/DON/".format(self.address)
        response = Messenger.get(extension, self.parent.authorization, self.ip)
        print("Sent the On command!")
        return

class Messenger():

    def get(extension, authorization, ip):
        url = ("http://{}{}".format(ip, extension))
        response = requests.get(url, auth=authorization)
        return (response)

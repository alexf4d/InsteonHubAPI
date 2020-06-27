import requests
import base64
from lxml import objectify, etree

from typing import List
import re


class ISY():
    #authorization = ""
    #ip = ""
    #nodes = {}
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

            self.nodes[node.name] = Node(self, name, node.address, node.type, node.property.get("formatted"), node.property.get("uom"))

    def get_node_status(self):

        ##### THIS IS THE PREFERED WAY AS IT IS ONLY ONE API CALL BUT DOESNT WORK BECAUSE NAME IS NOT PRESENT IN THE XML####
        # extension = "/rest/status"
        # response = Messenger.get(extension, self.authorization, self.ip)
        # xml = response.text.encode('utf8')
        # root = objectify.fromstring(xml)
        
        # self.status = {}
        # for node in root.iterchildren(tag='node'):
        #     self.status[node.name] = node.property.get("formatted") # add status to status dictionary
        #     self.nodes[node.name].status = node.property.get("formatted") # add status to node instance
        # return(status)  # return a dictionary of the status of nodes ['node_name': "status"]


        ##### THIS IS VERY SLOW AND NOT GOOD PRACTICE#####
        status = {}
        for node in self.nodes:
            status[self.nodes[node].name] = self.nodes[node].get_status()
        return(status)

    def get_scenes(self, method):
        """
        Gets available scenes from the hub.

        :param method: pass "name" for name referenced or "address" for address referenced
        :returns: Null
        """

        extension = "/rest/nodes/scenes"
        response = Messenger.get(extension, self.authorization, self.ip)
        xml = response.text.encode('utf8')
        root = objectify.fromstring(xml)

        self.scenes = {}

        for scene in root.iterchildren(tag='group'):
            if method == "name":
                name = str(scene.name)
            elif method == "address":
                name = str(scene.address)
            else:
                return

            self.scenes[scene.name] = Scene(self, name, scene.address)

    def create_listener(self):
        listener = Listener(self)
        return

class Node(ISY):

    def __init__(self, parent, name, address, category, status, properties):
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
    
    def get_status(self):
        extension = "/rest/status/{}".format(self.address)
        response = Messenger.get(extension, self.parent.authorization, self.parent.ip)
        xml = response.text.encode('utf8')
        root = objectify.fromstring(xml)
        self.status = root.property.get("formatted")
        return (self.status)

    def on(self):
        extension = "/rest/nodes/{}/cmd/DON/".format(self.address)
        response = Messenger.get(extension, self.parent.authorization, self.parent.ip)
        print("Sent the On command!")
        return

    def off(self):
        extension = "/rest/nodes/{}/cmd/DOF/".format(self.address)
        response = Messenger.get(extension, self.parent.authorization, self.parent.ip)
        print("Sent the Off command!")
        return

    def dimmer(self, value):
        if value not in range(0,100):
            print("Value must be between 0-100")
            return
        self.value = value
        extension = "/rest/nodes/{}/cmd/DON/{}".format(self.address,self.value)
        response = Messenger.get(extension, self.parent.authorization, self.parent.ip)
        print("Sent the Dimmer command!")
        return
    
    def low(self):
        extension = "/rest/nodes/{}/cmd/DON/25".format(self.address)
        response = Messenger.get(extension, self.parent.authorization, self.parent.ip)
        print("Sent the Slow command!")
        return
    
    def medium(self):
        extension = "/rest/nodes/{}/cmd/DON/75".format(self.address)
        response = Messenger.get(extension, self.parent.authorization, self.parent.ip)
        print("Sent the Medium command!")
        return

    def high(self):
        extension = "/rest/nodes/{}/cmd/DON/100".format(self.address)
        response = Messenger.get(extension, self.parent.authorization, self.parent.ip)
        print("Sent the High command!")
        return

class Scene(ISY):

    def __init__(self, parent, name, address):
        self.parent = parent
        self.name = name
        self.address = address
        #self.members = members

    def __str__(self):
        return str(self.name)
    
    ####THIS WILL HAVE TO BE MODIFIED TO ITERATE THROUGH MEMBERS STATUS#####
    # def get_status(self):
    #     extension = "/rest/status/{}".format(self.address)
    #     response = Messenger.get(extension, self.parent.authorization, self.parent.ip)
    #     xml = response.text.encode('utf8')
    #     root = objectify.fromstring(xml)
    #     self.status = root.property.get("formatted")
    #     return (self.status)

    def on(self):
        extension = "/rest/nodes/{}/cmd/DON/".format(self.address)
        response = Messenger.get(extension, self.parent.authorization, self.parent.ip)
        print("Sent the On command!")
        return

    def off(self):
        extension = "/rest/nodes/{}/cmd/DOF/".format(self.address)
        response = Messenger.get(extension, self.parent.authorization, self.parent.ip)
        print("Sent the Off command!")
        return

    def dimmer(self, value):
        if value not in range(0,100):
            print("Value must be between 0-100")
            return
        self.value = value
        extension = "/rest/nodes/{}/cmd/DON/{}".format(self.address,self.value)
        response = Messenger.get(extension, self.parent.authorization, self.parent.ip)
        print("Sent the Dimmer command!")
        return

class Messenger():

    def get(extension, authorization, ip):
        url = ("http://{}{}".format(ip, extension))
        response = requests.get(url, auth=authorization)
        return (response)

class Listener(ISY):
    # [ ] Listen for unsolicited feedback from the ISY Hub
    # [ ] Based on feedback update Node or Scene instances
    # [ ] Setup event handler to call user defined functions given a particular response
    def __init__(self, parent):
        self.parent = parent    




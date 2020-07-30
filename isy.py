import requests
import base64
from lxml import objectify, etree

from typing import List
import re

import socket


import websocket
import threading


class ISY():
    #authorization = ""
    #ip = ""
    #nodes = {}
    def __init__(self, username, password, ip):
        self.authorization = (username, password)
        self.ip = ip
    def get_nodes(self):
        """
        Gets available nodes from the hub.
        """

        extension = "/rest/nodes"
        response = Messenger.get(extension, self.authorization, self.ip)
        xml = response.text.encode('utf8')
        root = objectify.fromstring(xml)

        self.nodes = {}

        for node in root.iterchildren(tag='node'):
            self.nodes[node.name] = Node(self, node.name, node.address, node.type, node.property.get("formatted"), node.property.get("uom"))
            self.nodes[node.address] = self.nodes[node.name]

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

    def get_scenes(self):
        """
        Gets available scenes from the hub.
        """

        extension = "/rest/nodes/scenes"
        response = Messenger.get(extension, self.authorization, self.ip)
        xml = response.text.encode('utf8')
        root = objectify.fromstring(xml)

        self.scenes = {}

        for scene in root.iterchildren(tag='group'):
            self.scenes[scene.name] = Scene(self, scene.name, scene.address)

    def listen(self):
        listener = Listener(self)

        #Created the Threads
        t1 = threading.Thread(target=listener.listen, args=())
        #Started the threads
        t1.start()
        
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
        
        self.callback_function = None
    
    def __str__(self):
        return str(self.name)
    
    def subscribe(self, function):
        self.callback_function = function
    
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
    # [X] Listen for unsolicited feedback from the ISY Hub
    # [X] Based on feedback update Node or Scene instances
    # [X] Setup event handler to call user defined functions given a particular response
    def __init__(self, parent):
        self.parent = parent 

    def on_message(self, message):
        try:
            # print(message)
            root = objectify.fromstring(message)
            for root in root.iterchildren(tag='node'):
                self.address = root
            self.parent.nodes[self.address].get_status()
            callback = self.parent.nodes[self.address].callback_function
            if callback == None:
                return
            else:
                if callable(callback):
                    callback(self.parent.nodes[self.address])
                else:
                    print("Error : Callback function is not callable.")

            return
        except:
            pass

    def listen(self):
        version_str = "Sec-WebSocket-Version: 13"
        protocol_str = "Sec-WebSocket-Protocol: ISYSUB"

        message = self.parent.authorization[0]+":"+self.parent.authorization[1]
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        authorization_str = "Authorization: Basic " + base64_message

        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://"+self.parent.ip+"/rest/subscribe",
                                on_message = self.on_message,
                                header = [protocol_str, version_str, authorization_str]
                                )
        self.ws.run_forever()
    
class Finder():

    def find():
        
        msg = (
            "M-SEARCH * HTTP/1.1\r\n"
            "HOST:239.255.255.250:1900]\r\n"
            "MAN:ssdp:discover\r\n"
            "MX:1\r\n"
            "ST:urn:udi-com:device:X_Insteon_Lighting_Device:1\r\n"
            )

        # A tuple with broadcast ip and port
        serverAddress = ("239.255.255.250", 1900)
        # Create a datagram socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.sendto(msg.encode(), serverAddress)

        try:
            while True:
                data, addr = s.recvfrom(65507)
                return(addr[0])
        except socket.timeout:
            pass
'''
Example usage of the ISY module
Demonstrates how to use user defined callback functions for realtime feedback
'''

from isy import *
import getpass

print("Searching for ISY hub...")
ip = Finder.find()     # Auto discover IP Address of ISY hub
if ip == None:
    print("No ISY hub auto discovered.")
    ip = input("IP:")   #No Hub found in through UPnP discovery, ask user for IP
username = input("Username:")   # Ask user for Username to ISY hub
password = getpass.getpass("Password:") # Ask user for Password to ISY hub (Password hiden while typing in terminal)

hub = ISY(username, password, ip)   # Create instance of an ISY hub



hub.get_nodes() # Get the nodes from the hub
hub.get_scenes() # Get the scenes from the hub

hub.listen()    # Listen for unsolicited feedback from the hub


#--- Function to be triggered upon an event change of a subscribed node---#
def myfunc(node):
    print("Callback function triggered")
    print("The Node was:")
    print(node.name)
    print(node.status)

hub.nodes['3E 3C 3B 1'].subscribe(myfunc)   # Subscribe node to event changes
hub.nodes['Study-Light'].subscribe(myfunc)  # Subscribe node to event changes


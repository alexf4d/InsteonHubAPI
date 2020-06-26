'''
Example usage of the ISY module
'''

from isy import *
import getpass


username = input("Username:")   # Ask user for Username to ISY hub
password = getpass.getpass("Password:") # Ask user for Password to ISY hub (Password hiden while typing in terminal)
ip = input("IP address:") # Ask user for IP Address of the ISY hub

hub = ISY(username, password, ip)   # Create instance of an ISY hub
hub.get_nodes("name") # Get the nodes from the hub; "name" = name referenced, "address" = Address referenced 

print("List of Nodes:")
print(hub.nodes)    # Print all Node objects (Name:Object)

for node in hub.nodes:
    print("\n Properties available to {}:".format(node))
    print(hub.nodes[node].properties)   # Print all the properites available to each node

    # Try to turn each node ON
    if hub.nodes[node].properties['On']:    # If node has "On" property try turning it on
        hub.nodes[node].on()

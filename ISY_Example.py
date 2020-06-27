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
hub.get_scenes("name") # Get the scenes from the hub; "name" = name referenced, "address" = Address referenced 

print("List of Nodes:")
print(hub.nodes)    # Print all Node objects (Name:Object)

for node in hub.nodes:
    print("\n Properties available to {}:".format(node))
    print(hub.nodes[node].properties)   # Print all the properites available to each node

    # Try to turn each node ON
    # if hub.nodes[node].properties['On']:    # If node has "On" property try turning it on
    #     hub.nodes[node].on()

print("\n Scenes available:")
for scene in hub.scenes:
    print(hub.scenes[scene].name)   # Print all scenes found

#If scene/node name is known it can be called like this as an example:    
    
    #NODES: available methods for node can be seen by calling .properties
    #hub.nodes['Kitchen-Light'].on()                    # turn 'Kitchen-Light on
    #hub.nodes['Kitchen-Light'].off()                   # turn 'Kitchen-Light off
    #hub.nodes['Kitchen-Light'].dimmer(35)              # turn 'Kitchen-Light to 35%
    #status = hub.nodes['Kitchen-Light'].get_status()   # Get the status of 'Kitchen-Light'
    #hub.nodes['Living Room-Fan'].low()                 # turn 'Living Room-Fan' on Low
    #hub.nodes['Living Room-Fan'].medium()              # turn 'Living Room-Fan' on Medium
    #hub.nodes['Living Room-Fan'].high()                # turn 'Living Room-Fan' on High
    #hub.nodes['Living Room-Fan'].off()                 # turn 'Living Room-Fan' off

    #SCENES:
    #hub.scenes['Home Scene'].on()                      # turn 'Home Scene' on
    #hub.scenes['Home Scene'].off()                     # turn 'Home Scene' off
    #hub.scenes['Home Scene'].dimmer(35)                # turn 'Home Scene' to 35%



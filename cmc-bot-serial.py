import time
import sys
import requests
import json
from pubsub import pub
from meshtastic.serial_interface import SerialInterface
from meshtastic import portnums_pb2

serial_port = '/dev/ttyACM0'  # Replace with your Meshtastic device's serial port

def get_node_info(serial_port):
    print("Initializing SerialInterface to get node info...")
    local = SerialInterface(serial_port)
    node_info = local.nodes
    local.close()
    print("Node info retrieved.")
    return node_info

def parse_node_info(node_info):
    print("Parsing node info...")
    nodes = []
    for node_id, node in node_info.items():
        nodes.append({
            'num': node_id,
            'user': {
                'shortName': node.get('user', {}).get('shortName', 'Unknown')
            }
        })
    print("Node info parsed.")
    return nodes

def on_receive(packet, interface, node_list):
    try:
        if packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message = packet['decoded']['payload'].decode('utf-8')
            fromnum = packet['fromId']
            shortname = next((node['user']['shortName'] for node in node_list if node['num'] == fromnum), 'Unknown')
            print(f"{shortname}: {message}")

            # 1. Define your variables and webhook URL
            # NOTE: Replace 'YOUR_DISCORD_WEBHOOK_URL_HERE' with your actual Discord webhook URL
            DISCORD_WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL_HERE' 

            # 2. Structure the data for Discord
            # The 'username' field sets the name displayed on the message.
            # The 'content' field is the main message text.
            # You can also add 'avatar_url' for a custom icon.
            payload = {
                "username": shortname,
                "content": message
            }

            # 3. Define the HTTP headers
            # Webhooks typically require the Content-Type header to be 'application/json'
            headers = {
                'Content-Type': 'application/json'
            }

            # 4. Send the POST request
            try:
                response = requests.post(
                    DISCORD_WEBHOOK_URL, 
                    data=json.dumps(payload), 
                    headers=headers
                )
                
                # 5. Check the response status
                if response.status_code == 204:
                    print("✅ Message successfully sent to Discord.")
                else:
                    print(f"❌ Failed to send message. Status code: {response.status_code}")
                    print(f"Response text: {response.text}")

            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

    except KeyError:
        pass  # Ignore KeyError silently
    except UnicodeDecodeError:
        pass  # Ignore UnicodeDecodeError silently

def main():
    print(f"Using serial port: {serial_port}")

    # Retrieve and parse node information
    node_info = get_node_info(serial_port)
    node_list = parse_node_info(node_info)

    # Print node list for debugging
    print("Node List:")
    for node in node_list:
        print(node)

    # Subscribe the callback function to message reception
    def on_receive_wrapper(packet, interface):
        on_receive(packet, interface, node_list)

    pub.subscribe(on_receive_wrapper, "meshtastic.receive")
    print("Subscribed to meshtastic.receive")

    # Set up the SerialInterface for message listening
    local = SerialInterface(serial_port)
    print("SerialInterface setup for listening.")
    print("Cornwall Meshtastic Community Bot has started.")

    # Keep the script running to listen for messages
    try:
        while True:
            sys.stdout.flush()
            time.sleep(1)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        print("Script terminated by user")
        local.close()

if __name__ == "__main__":
    main()
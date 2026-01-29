from opcua import Client, ua
import time

NODE_STATUS = "ns=1;s=uart_status"

def connect_with_retry(ip_address: str, port: str, retries: int = 3) -> Client | None:
    url = f"opc.tcp://{ip_address}:{port}"
    
    for attempt in range(1, retries + 1):
        try:
            print(f"Connecting to {url} (Attempt {attempt}/{retries})...")
            client = Client(url)
            
            client.set_user("")
            client.set_password("")
            
            client.connect()
            return client
            
        except Exception as e:
            print(f"Connection failed: {e}")
            if attempt < retries:
                time.sleep(2)
            else:
                return None

def node(node_number: int) -> str:
    return f"ns=1;s=IN{node_number}_control"

def read_server_status(client) -> str | None:
    try:
        node = client.get_node(NODE_STATUS)
        val = node.get_value()
        print(f"[SERVER STATUS]: {val}")
        return val
    except Exception as e:
        print(f"Error reading status: {e}")
        return None


def switch_inputs(client: Client, node_command_id, out_choose: int) -> str | float:
    # 1. Handle the input if it comes as an integer (like in your error image)
    if isinstance(node_command_id, int) or (isinstance(node_command_id, str) and node_command_id.isdigit()):
        # Convert integer '1' to string "ns=1;s=IN1_control"
        node_str = f"ns=1;s=IN{node_command_id}_control"
    else:
        # Assume it is already the full string
        node_str = str(node_command_id)

    try:
        node_command = client.get_node(node_str)
        node_command.set_value(ua.Variant(out_choose, ua.VariantType.Int32)) 

        result = read_server_status(client)
        if result is None:
            return -999.0
        return result

    except Exception as e:
        print(f"Error in switch_inputs: {e}")
        return -999.0 

def disconnect(client: Client) -> None:
    if client:
        try:
            client.disconnect()
            print("Disconnected successfully.")
        except Exception as e:
            print(f"Error disconnecting: {e}")

if __name__ == "__main__":
    TARGET_IP = "192.168.88.120"
    TARGET_PORT = "4840"

    client = connect_with_retry(TARGET_IP, TARGET_PORT)
    
    if client:
        print("Connected to OPC UA server.")
        
        target_node_id = node(1) 
        
        switch_inputs(client, 1, 5)

        time.sleep(1)

        disconnect(client)
    else:
        print("Failed to connect to OPC UA server.")
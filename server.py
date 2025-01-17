
import xmlrpc.server
import xmlrpc
import threading

class Process:
    def __init__(self, name, is_faulty=False):
        self.name = name
        self.is_faulty = is_faulty
        self.messages = {}

    def send_message(self, recipient_name, decision):
        """ simulates the process of sending a message in a distributed system,
        with special behavior for a faulty process (specifically P) 
        to exhibit malicious activity such as denying to receive messages from R and S
        """
        if self.is_faulty and self.name == "P" and recipient_name in ["R", "S"]:
            print(f"Process {self.name} is denying communication to {recipient_name}")
            return f"{self.name} denied communication to {recipient_name}"
        # creating a dynamic link that uses:
        # P's port, unicode value of recipient_name minus the unicode value of P
        # eg; 8000 + 81 for Q - 80 for P we get port 8001 which will be the recipients port
        recipient_proxy = xmlrpc.client.ServerProxy(f"http://localhost:{8000 + ord(recipient_name) - ord('P')}/")
        print(f"{self.name} sent decision '{decision}' to {recipient_name}") 
        recipient_proxy.receive_message(self.name, decision)
    
        return f"{self.name} sent decision '{decision}' to {recipient_name}"

    def receive_message(self, sender, decision) -> str:
            # Only process messages if the process is not faulty
        if self.is_faulty:
            return f"{self.name} (faulty) ignored message from {sender}"
        self.messages[sender] = decision
        print(f"{self.name} received decision '{decision}' from {sender}")
        return f"{self.name} received decision '{decision}' from {sender}"

    def finalize_decision(self) -> str:
        if self.is_faulty:
            return "faulty"

        decisions = list(self.messages.values())
        majority = max(set(decisions), key=decisions.count)
        print(f"majority is : {majority}")
        
        return majority

def run_server(name, port, is_faulty):
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", port))
    server.register_instance(Process(name, is_faulty))
    print(f"Process {name} running on port {port}...")
    server.serve_forever()

if __name__ == "__main__":
    processes = [
        {"name": "P", "port": 8000, "is_faulty": True},
        {"name": "Q", "port": 8001, "is_faulty": False},
        {"name": "R", "port": 8002, "is_faulty": False},
        {"name": "S", "port": 8003, "is_faulty": False},
    ]

    for process in processes:
        threading.Thread(target=run_server, args=(process["name"], process["port"], process["is_faulty"])).start()

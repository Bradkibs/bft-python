
import xmlrpc.server
import xmlrpc
import threading

class Process:
    def __init__(self, name, is_faulty=False):
        self.name = name
        self.is_faulty = is_faulty
        self.messages = {}

    def send_message(self, recipient_name, decision) -> str:
        if self.is_faulty:
            decision = "arbitrary decision"  
        # Simulating the sending message action to another process by RPC
        recipient_proxy = xmlrpc.client.ServerProxy(f"http://localhost:{8000 + ord(recipient_name) - ord('P')}/")
        recipient_proxy.receive_message(self.name, decision)
        return f"{self.name} sent decision '{decision}' to {recipient_name}"

    def receive_message(self, sender, decision) -> str:
        self.messages[sender] = decision
        return f"{self.name} received decision '{decision}' from {sender}"

    def finalize_decision(self) -> str:
        if self.is_faulty:
            return "faulty"

        decisions = list(self.messages.values())
        majority = max(set(decisions), key=decisions.count)
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

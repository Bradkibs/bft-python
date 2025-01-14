
import xmlrpc.client
import time

if __name__ == "__main__":

    processes = {
        "P": xmlrpc.client.ServerProxy("http://localhost:8000/"),
        "Q": xmlrpc.client.ServerProxy("http://localhost:8001/"),
        "R": xmlrpc.client.ServerProxy("http://localhost:8002/"),
        "S": xmlrpc.client.ServerProxy("http://localhost:8003/"),
    }


    decisions = ["attack", "retreat"]
    for sender_name, sender_proxy in processes.items():
        for recipient_name, recipient_proxy in processes.items():
            if sender_name != recipient_name:
                decision = decisions[0]  # 0 for "attack" or 1 for "retreat"
                sender_proxy.send_message(recipient_name, decision)
                time.sleep(0.1)


    for name, proxy in processes.items():
        print(f"Process {name} finalized decision: {proxy.finalize_decision()}")

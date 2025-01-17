# Byzantine Fault Tolerance Simulation

This project simulates a distributed system based on the Byzantine Generals analogy, where four processes (P, Q, R, and S) attempt to reach an agreement on a task. Process P is intentionally made faulty to demonstrate malicious behavior, specifically denying communication with other processes (R and S). The system uses XML-RPC (Remote Procedure Calls) to facilitate inter-process communication.

## Table of Contents

- [Overview](#overview)
- [Files](#files)
- [Setup Instructions](#setup-instructions)
- [Running the Code](#running-the-code)
- [Expected Output](#expected-output)
- [Explanation](#explanation)
- [License](#license)

## Overview

In a distributed system, processes need to reach an agreement despite the presence of faulty or malicious actors. This simulation represents a scenario where:

- Process **P** is intentionally faulty (malicious) and denies communication with certain other processes.
- Processes **Q**, **R**, and **S** are non-faulty and attempt to communicate with each other to reach a consensus.

The system uses XML-RPC servers and clients to simulate the communication between processes. The goal is to illustrate how processes attempt to finalize a decision despite the faulty behavior of process P.

## Files

- **`server.py`**: Contains the logic for the processes (P, Q, R, and S) to communicate with each other and make a decision. Process P exhibits faulty behavior by denying communication with other processes.
- **`client.py`**: Sends messages from each process to the others, simulates decision-making, and finalizes the agreement based on the received messages.

## Setup Instructions

1. **Clone the Repository**:

```

git clone <repo url which should end with .git>
cd <repo directory name>

```

2. **Install Python (if not already installed)**:
   Ensure that Python 3.x is installed on your machine. You can download it from [python.org](https://www.python.org/).

3. **Install Required Libraries**:
   You can install the required libraries using `pip`:

```

pip install xmlrpc

```

## Running the Code

1. **Start the Server**:
   To simulate the processes, first run the server script. This will start each process (P, Q, R, and S) on different ports.

```bash
python server.py
```

2. **Run the Client**:
   In another terminal, run the client script. The client will attempt to send decisions to each of the other processes and finalize the decision based on the responses.

   ```bash
   python client.py
   ```

## Expected Output

After running the server and client scripts, the following output will be generated:

### Output from `server.py`:

```
Process P running on port 8000...
Process Q running on port 8001...
Process R running on port 8002...
Process S running on port 8003...
```

### Output from `client.py`:

```
Process P denied communication to Q
Process P denied communication to R
Process P denied communication to S
Process Q sent decision 'attack' to P
Process Q sent decision 'attack' to R
Process Q sent decision 'attack' to S
Process R sent decision 'attack' to P
Process R sent decision 'attack' to Q
Process R sent decision 'attack' to S
Process S sent decision 'attack' to P
Process S sent decision 'attack' to Q
Process S sent decision 'attack' to R
Process P finalized decision: faulty
Process Q finalized decision: attack
Process R finalized decision: attack
Process S finalized decision: attack
```

As you can see, Process P denies communication to the other processes (Q, R, S). The remaining processes (Q, R, S) successfully communicate and agree on the decision "attack."

## Explanation

### `server.py`

- **Process Class**:

  - Represents each process in the system.
  - `send_message()`: Simulates sending a decision to another process. If the process is P and it is faulty, it denies communication with certain processes.
  - `receive_message()`: Receives messages from other processes and stores them.
  - `finalize_decision()`: Finalizes the decision by determining the majority decision from the messages received.

- **Server Logic**:

  - Each process runs on a different port, and a `SimpleXMLRPCServer` is created for each process. The server listens for incoming requests and handles message exchanges.

- **Faulty Process P**:
  - The faulty process (P) intentionally denies communication to processes R and S, simulating malicious behavior. It is configured to be faulty when initializing the `Process` class.

### `client.py`

- **Client Logic**:
  - Sends decisions from each process to every other process. After all processes send their messages, each process finalizes its decision based on the majority vote.
  - In this simulation, the client serves to trigger the message exchange and decision-making process.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

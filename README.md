# Distributed Vector Clock Messaging System

## Project Overview

This repository contains the implementation of a Distributed Vector Clock Messaging System. The project is divided into two parts: Unicast Messaging and Broadcast Messaging. The objective is to demonstrate the transmission of messages between processes in a distributed system and to update and display vector clocks for each process.

## Objectives

### Part 1: Unicast Message
The goal is to enable each process to transmit a unicast message to another process, update each process's vector clock, and print the vector clock both before and after sending/receiving messages.

### Part 2: Broadcast Message
The aim is to enable each process to broadcast a message to all other processes, update their vector clocks, and print the vector clocks both before and after sending/receiving messages.

## Implementation

### Libraries Used
- `sys`
- `threading`
- `socket`
- `time`
- `random`
- `pickle`

### Key Functions and Methods
- **EventList**: A list to save and display the vector clock of each process at each event.
- **vector_max(vector1, vector2)**: Computes the maximum values for the vector clock updates.
- **handler(conn, addr)**: Handles connections, prints the vector clock before and after sending/receiving messages.
- **listen(node)**: Listens for messages and connects multiple threads.

### Usage

#### Unicast Messaging
1. Run `clock.py`.
2. Enter a unique port number and a process ID (1, 2, or 3).
3. Enter the receiver's port number, sender event number, and receiver event number to send a message.
4. The vector clock of the specific process is updated and displayed before and after sending/receiving messages.

#### Broadcast Messaging
1. Run `clock.py`.
2. Enter a unique port number and a process ID (1, 2, or 3).
3. Send a broadcast message to all processes.
4. The vector clock of each process is updated and displayed before and after sending/receiving messages.

### Output
The outputs display the vector clocks of processes before and after each message transmission.

### How to Run
PART 1

Installation:
pip install socket
pip install datetime

Execute Insructions:
Step1: Run the clock1.py file from the 'Part 1' folder using command 'python clock1.py'

Testing Instructions:
Run clock1.py file on terminal.
Assign each program a unique port number.
Provide the values as per instructions on the terminal.

PART 2

Installation:
pip install socket
pip install datetime

Execute Insructions:
Step1: Run the clock2.py file from the 'Part 2' folder using command 'python clock2.py'

Testing Instructions:
Run clock2.py file on terminal.
Assign each program a unique port number.
Provide the values as per instructions on the terminal.

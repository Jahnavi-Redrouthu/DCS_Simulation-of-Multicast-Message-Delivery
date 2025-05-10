from simulator import *
from collections import deque

# List of multicast events (time, message_id, sending host_id, payload)
multicast_events = [
    (10, 'M1', 1, 'rupa'),
    (20, 'M2', 1, 'satwi'),
    (30, 'M3', 1, 'janu'),
    (10, 'M4', 2, 'One'),
    (20, 'M5', 2, 'Two'),
    (30, 'M6', 2, 'Three')
]

# Custom message class definition
class CustomMessage:
    def __init__(self, message_id, src, dst, payload, sequence_number=None):
        self.message_id = message_id
        self.src = src
        self.dst = dst
        self.payload = payload
        self.sequence_number = sequence_number

# Host class representing a node in the simulation
class HostNode(Node):
    def __init__(self, sim, host_id):
        Node.__init__(self, sim, host_id)
        self.host_id = host_id
        self.group_members = []  # Group members (all hosts in the simulation)
        self.sequencer = None  # Host responsible for message sequencing
        self.message_queue = deque()  # Queue to hold received messages
        self.next_delivery_sequence = 0  # Next sequence number for message delivery
        self.delivered_messages = set()  # Set to track delivered message IDs

    def initialize_host(self):
        # Set the sequencer to be the first member of the group
        self.sequencer = self.group_members[0]

    def send_multicast(self, time, message_id, payload):
        # Sending a multicast message to the sequencer
        print(f'Time {time}:: {self} SENDING multicast message [{message_id}]')
        
        # Create a CustomMessage and send it to the sequencer
        mcast = CustomMessage(message_id, self, self.sequencer, payload)
        self.send_message(self.sequencer, mcast)

    def receive_message(self, frm, message, time):
        # Handling received messages
        print(f'Time {time}:: {self} RECEIVED message [{message.message_id}] from {frm}')

        if frm == self.sequencer:
            # If message is from sequencer, process it for delivery
            self.process_message_for_delivery(time, message)
        elif frm != self:
            # If message is from another host, forward it to the sequencer for ordering
            self.send_message(self.sequencer, message)  # No duplicate check needed

    def process_message_for_delivery(self, time, message):
        # Assign sequence number if not already assigned
        if message.sequence_number is None:
            message.sequence_number = self.next_delivery_sequence
            self.next_delivery_sequence += 1

        # Add message to the queue and deliver in order
        self.message_queue.append(message)
        
        while self.message_queue:
            msg = self.message_queue[0]
            if msg.message_id not in self.delivered_messages:
                self.delivered_messages.add(msg.message_id)
                self.message_queue.popleft()
                print(f'Time {time:4}:: {self} DELIVERED message [{msg.message_id}] -- {msg.payload}')
            else:
                break  # Stop delivering if message is already delivered

# Driver class to run the simulation
class SimulationDriver:
    def __init__(self, sim):
        self.hosts = []  # List to hold host instances
        self.sim = sim  # Simulation instance

    def setup_hosts_and_run(self, num_hosts=3):
        # Create host instances
        for i in range(num_hosts):
            host = HostNode(self.sim, i)
            self.hosts.append(host)

        # Set group members for each host and initialize
        for host in self.hosts:
            host.group_members = self.hosts
            host.initialize_host()

        # Schedule multicast events for each host
        for event in multicast_events:
            time = event[0]
            message_id = event[1]
            host_id = event[2]
            payload = event[3]
            self.sim.add_event(Event(time, self.hosts[host_id].send_multicast, time, message_id, payload))

def start_simulation():
    # Create simulation instance
    simulator = Simulator(debug=False, random_seed=1233)

    # Start the driver and run the simulation with 5 hosts
    driver = SimulationDriver(simulator)
    driver.setup_hosts_and_run(num_hosts=5)

    # Start the simulation
    simulator.run()

if __name__ == "__main__":
    start_simulation()

from simulator import *

class HostNode(Node):
    def __init__(self, sim, node_id, name=''):
        super().__init__(sim, node_id, name)
        self.host_id = node_id

    def receive_message(self, sender, message, timestamp):
        if message.message_type == 'PING':
            print(f'{timestamp} :: {self} received PING from {sender}')
            print(f'{timestamp} :: {self} sending PONG to {sender}')
            pong_message = Message(message.message_id, self, message.src, 'PONG')
            self.send_message(sender, pong_message)
        elif message.message_type == 'PONG':
            print(f'{timestamp} :: {self} received PONG from {sender}')

def main():
    # Create an instance of the simulator
    sim = Simulator(debug=False, random_seed=234)

    # Create two host nodes within the simulation
    host1 = HostNode(sim, 1)
    host2 = HostNode(sim, 2)

    # Define messages to be exchanged between hosts
    ping_message1 = Message(1, host1, host2, 'PING')
    ping_message2 = Message(2, host2, host1, 'PING')
    
    # Initiate the first PING message from host1 to host2
    print(f'{sim.time} :: {host1} is sending PING to {host2}')
    host1.send_message(host2, ping_message1)
    
    # Define a function to send a PING message from host2 to host1 after a delay
    def send_ping_to_host1():
        print(f'{sim.time} :: {host2} is sending PING to {host1}')
        host2.send_message(host1, ping_message2)

    # Schedule a timer to execute the function after 100 simulation time units
    timer1 = Timer(sim, 100, send_ping_to_host1)
    timer1.start()

    # Schedule another timer using a shorter syntax after 200 simulation time units
    timer2 = Timer(sim, 200, host2.send_message, host1, ping_message2)
    timer2.start()

    # Start the simulation, which runs until completion
    sim.run()                 

if __name__ == "__main__":
    main()

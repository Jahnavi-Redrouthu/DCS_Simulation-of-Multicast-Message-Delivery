import heapq
import random

class Message:
    def __init__(self, message_id, src, dest, message_type, payload=None):
        self.message_id = message_id
        self.src = src
        self.dest = dest
        self.message_type = message_type
        self.payload = payload
     
    def __str__(self):
        return f'{self.message_id} Type {self.message_type}::{self.src}=>{self.dest}--[{self.payload}]' if self.payload else f'{self.message_id} Type {self.message_type}::{self.src}=>{self.dest}'

class Event:
    def __init__(self, time, callback, *args, **kwargs):
        self.event_time = time
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
    
    def __lt__(self, other):
        return self.event_time < other.event_time

    def execute(self):
        func = self.callback
        if self.args and self.kwargs:
            func(*self.args, **self.kwargs)
        elif self.args:
            func(*self.args)
        elif self.kwargs:
            func(**self.kwargs)
        else:
            func()

class Timer:
    def __init__(self, simulator, interval, callback, *args, **kwargs):
        self.simulator = simulator
        self.interval = interval
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
    
    def start(self):
        event = Event(self.simulator.time + self.interval, self.callback, *self.args, **self.kwargs)
        self.simulator.add_event(event)

class Node:
    def __init__(self, simulator, node_id, name=''):
        self.simulator = simulator
        self.node_id = node_id
        self.name = name
        self.alive = True
        
    def get_id(self):
        return self.node_id
        
    def send_message(self, to_node, message):
        if not self.alive:
            return
        
        if self.simulator.debug: 
            print(f'DEBUG {self} sending message [{message.message_id}] to {to_node}') 
        
        self.simulator.send_message(self, to_node, message)
    
    def receive(self, time, sender, message):
        if not sender.alive:
            return
        
        if self.simulator.debug:
            print(f'DEBUG Time {time}:: {self} received message {message} from {sender}')
        
        self.receive_message(sender, message, time)
        
    def receive_message(self, sender, message, time):
        raise NotImplementedError('receive_message function is not implemented')
        
    def is_alive(self):
        return self.alive
        
    def failed(self):
        self.alive = False
    
    def recovered(self):
        self.alive = True
              
    def __hash__(self):
        return self.node_id

    def __str__(self):
        if self.name:
            return f'Node-{self.name}'
        else:
            return f'Node-{self.node_id}'    

class Simulator:
    def __init__(self, debug=True, random_seed=1234):
        self.debug = debug 
        self.events = []
        self.time = 0
        self.max_latency = 100
        self.random_generator = random.Random(random_seed)
        
    def add_event(self, event):
        heapq.heappush(self.events, event)

    def send_message(self, src_node, dest_node, message):
        delay = self.random_generator.randint(1, self.max_latency)
        event_time = self.time + delay
        event = Event(event_time, dest_node.receive, event_time, src_node, message)
        self.add_event(event)
                
    def run(self):
        while self.events:
            event = heapq.heappop(self.events)
            self.time = event.event_time
            event.execute()
        print(f'Simulation ended at time {self.time}')

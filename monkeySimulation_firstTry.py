import simpy

NEW_MONKEYS = 5 #Assuming there are 5 monkeys
env = simpy.Environment()

#placement and monkeystore are resources.
placement = simpy.Resource(env, capacity=5) 
monkeystore = [simpy.Resource(env, 1)
               for _ in range(5)]
#for _ in range(5) so that objects of monkeystore resources can be indexed

#Class MonkeyProcesses to define processes (actions that monkeys do)
class MonkeyProcesses:
    #initialization
    def __init__(self, env, name, destroytime, placement, monkeystore):
        self.env = env
        self.name = name
        self.placement = placement
        self.monkeystore = monkeystore
        self.destroytime = destroytime
        self.completion = env.event()

    #Assuming this process will be executed till destroytime
    def destroylink(self):
        print('%s arrived at %s' % (self.name,(self.env.now)))
        yield env.timeout(self.destroytime)
        print(' destroyed link at %s' % (self.env.now))

    def destroynode(self):
        print('%s arrived at %s' % (self.name,(self.env.now)))
        yield env.timeout(self.destroytime)
        print(' destroyed node at %s' % (self.env.now))
        
#This controls which monkeys execute which process.
#(Only two processes are defined for now,even though there are 5 monkeys). For the last 3 processes, "no more processes" will be printed
def user(env, monkey, number):
    for i in range(number): 
        monkey = monkeys[i]
        if i==0 :
            with placement.request() as req:
                yield env.process(monkey.destroylink())
            
        elif i==1 :
            with placement.request() as req:
                yield env.process(monkey.destroynode())

        else:
            print ('No more process')
            
#Creating 5 objects         
monkeys = [ MonkeyProcesses(env, 'Monkey A', 2, placement, monkeystore[0]),
            MonkeyProcesses(env, 'Monkey B', 1, placement, monkeystore[1]),
            MonkeyProcesses(env, 'Monkey C', 2, placement, monkeystore[2]),
            MonkeyProcesses(env, 'Monkey D', 3, placement, monkeystore[3]),
            MonkeyProcesses(env, 'Monkey E', 5, placement, monkeystore[4]),
    ]

#Creating instance of process
env.process(user(env,monkeys,NEW_MONKEYS))
#Start event
env.run()

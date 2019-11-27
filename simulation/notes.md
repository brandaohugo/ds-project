# Discrete event simulation

## components

Resources:
Entities:
Processes:

# simpy specifics
all components modelled with processes (described by generators).
all proc live in an environment.
proc interact with environment and eachother via events.

# process interactions
The Process instance that is returned by Environment.process() can be utilized for process interactions. The two most common examples for this are to wait for another process to finish and to interrupt another process while it is waiting for an event.

# requirements

simulation that simulates a system, specific transactions do not matter.

input coming in, with certain distribution, we can change distribution. Flow is processed. 

Different types of processes can be simulated

think about read write operations, modelling a database of transactions.

stochastic input coming in. 

2 - 5 jobs minimum.

should resemble a system that does transaction handling

timeseries data should be coming out. 

indication of normal behaviour and abnormal behaviour. 
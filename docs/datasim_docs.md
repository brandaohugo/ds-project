# DataSim Documentation

## Application Architecture

Flask application which programatically generates discrete-event simulations of server cluster interactions, with a specific focus on transaction processing. The user is able to specify the parameters and topology of the desired simulation through a `JSON` configuration file, as well as the ability to introduce errors into the system. This file is passed into the application as part of a `POST` request, whereafter it is parsed and the simulation is executed.

```javascript
# config.json example

{
  "simulation_name": "Simulation1",
  "simulation_time": 600,
  "server": {
    "name": "Load Balancer",
    "trs_per_sec": 25,
    "rand_server_freeze": true,
    "server_freeze_time": 15,
    "number": 5
  },
  "user": {
    "user_number": 200,
    "prob_dist": "gaussian"
  }
}
```
Furthermore, the application contains a user registration system and saves simulation data associated with each user to a local database. Each simulation run is logged and accessible to the user, along with the ability to visualise simulation results as well as the topology and settings used for each respective run.

## Simulations

### 1. User Requests

#### 1.1 Description

This simulation currently models the interaction between multiple users and one server. Each user makes a request to a server, whereafter the server accepts the request if it has free available slots. Each request takes a given amount of time to process, which is dependent on how fast new users are being generated, the processing speed of the server as well as the size of the payload that the user submits to the server for processing. 

#### 1.2 Parameters

`SIM_TIME`: Time for which simulation will run.<br>
`GEN_INTER`: New user generation time interval.<br>
`PAYLOAD_SIZE`: User request processing load size in mb.<br>
`PROCESS_SPEED`: Server payload processing speed in mb/second.<br> 
`CONC_USERS`: Number of concurrent users that can access servers.

#### 1.3 Behaviour

- Changing number of `CONC_USERS` can result in queues forming. The same holds for 'GEN_INTER'.

- Varying `PROCESS_SPEED` of server directly impacts the time taken to process requests.

- Varying `PAYLOAD_SIZE` also has an effect on when server slot is available again as it affects the time taken to process the request.

## Error Types

### Deadlock 

### Server freeze

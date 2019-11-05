# ING Discrete Event Simulation

## How to run the enviroment

### Prepare the enviroment

Create a virtualenviroment with the required packages
```sh
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Define the Flask Application

```sh
$ export FLASK_APP=datsim
$ export FLASK_ENV=development
```

Initialize the database
```sh
$ flask db-init
``

Run the Application

```sh
$ flask run
```



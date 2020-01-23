# DataSim Discrete Event Simulator

## Getting started

### On Localhost 

Create a virtualenviroment with the required packages
```sh
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Define the Flask Application

```sh
$ export FLASK_APP=datasim
$ export FLASK_ENV=development
```

Initialize the database
```sh
$ flask init-db
```

Run the Application

```sh
$ flask run
```

### Docker

- Download Docker

- Download this repository `git clone https://github.com/brandaohugo/ds-project.git`

- Go the directory of this project and build the docker image `sudo docker build -t datasim:latest .`

- Run the container using `sudo docker run -d -p 5000:5000 datasim:latest`

- Go to `localhost:5000` to use the application.



# Python Kafka Example

Example Python App Consuming and Producing to Kafka topic

## Environment Setup

Follow the instructions below to configure your local machine to run and develop this example Python application.

_Note:_ The instructions are focused on MacOsx however other environments will be supported with a bit of googling.

### Local Docker Environment
The example code relies on a running Kafka service, the repo contains a Docker compose file that will spin up a configured Kafka.

* Install Docker Toolbox - [Instructions](https://www.docker.com/products/docker-toolbox)

* Run the docker environment `docker-compose up`

This will launch a kafka service listening on port `9092` initialised with a Topic called `messages`

### Build dependencies

* Python 3 `$ brew install python3`
* Virtual Env `$ sudo pip3 install virtualenv`

### Configure and Run

From the terminal enable & configure the application dependencies.
* `$ virtualenv env`
* `$ source env/bin/activate`
* `(env) $ pip3 install -r requirements.txt`

You can now run the application
* `(env) $ python3 kafka-example`

To leave the virtual Environment
* `(env) $ deactivate`

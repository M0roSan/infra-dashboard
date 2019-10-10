This project is not up-to-date. It is moved to GitLab to leverage CICD pipeline.
GitLab->ECR->ECS. 

# infra-dashboard
infrastructure dashboard leveraging docker and aws

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

install python3.7 and pip3  
install Docker for [Mac](https://docs.docker.com/docker-for-mac/install/) or [Windows](https://docs.docker.com/docker-for-windows/) *You need Windows Pro version. recommend run your project locally or install linux on VM*

### Installing

source scripts or add scripts into your .bashrc file for easier bash experience.  
Make sure to change the first line to absolute path of the infra-dashboard (e.g. in Mac, /Users/masa/infra-dashboard)
```
source .dev_scripts.sh
```

To up and run the banken 

```
start-banken
```
If you specifically want to run the container, append its name after start-banken
```
start-banken api-server
```
To stop the banken containers
```
stop-banken
```

install python major dependencies for the project if you run python project without using docker 
```
pip3 install -r requirements.txt
```
To modify each python module, go into each directory and create virtualenv using following command
```
python3 -m venv ./venv
source venv/bin/activate
pip3 install -r requirements.txt
```
To deactivate
```
deactivate
```
When pip3 installing new modules to its venv, make sure to freeze it into requirements.txt
```
pip3 freeze > requirements.txt
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

To run unit test
```
python3 -m pytest
```


### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Use Flake8 to code and style python code
```
python3 -m flake8 --max-line-length=120
```

## Deployment

Add additional notes about how to deploy this on a live system

# infra-dashboard
infrastructure dashboard leveraging docker and aws

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

install python3.7 and pip3  
install python major dependencies for the project
```
pip install -r requirements.txt
```
To modify each python module, go into each directory and create virtualenv using following command
```
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```
To deactivate
```
deactivate
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
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

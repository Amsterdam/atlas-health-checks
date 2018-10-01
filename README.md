# Atlas health checks

Collection of tests that validate APIs are healthy.
Anonymous and authenticated requests are send to end points used by Atlas (City Data) project.

## Install
```
pip install -r requirements.txt
```

## Run / tests

The following environment variables should be set:
```
USERNAME_EMPLOYEE_PLUS
PASSWORD_EMPLOYEE_PLUS
```

Run on development system:
```
pytest
```

or run inside docker container with:

```
docker-compose up
``` 

# Charge Points API


##  Description

A simple API for charge points.

###  Directory Structure
```
ampcontrol
├─ app
│  ├─ api
│  │  ├─ api_v1
│  │  │  ├─ api.py
│  │  │  └─ endpoints
│  │  │     ├─ auth.py
│  │  │     └─ charge_points.py
│  │  ├─ deps
│  │  │  ├─ charge_point.py
│  │  │  ├─ db.py
│  │  │  └─ user.py
│  │  └─ root.py
│  ├─ core
│  │  ├─ application.py
│  │  ├─ config.py
│  │  ├─ logger.py
│  │  └─ users.py
│  ├─ crud
│  │  ├─ base.py
│  │  └─ charge_point.py
│  ├─ db
│  │  ├─ base.py
│  │  ├─ base_class.py
│  │  ├─ exceptions.py
│  │  └─ session.py
│  ├─ main.py
│  ├─ models
│  │  ├─ charge_point.py
│  │  └─ user.py
│  ├─ schemas
│  │  ├─ base.py
│  │  ├─ charge_point.py
│  │  └─ user.py
│  └─ tests
│     ├─ conftest.py
│     ├─ endpoints
│     │  ├─ charge_point_test.py
│     │  └─ root_test.py
│     └─ utils
│        ├─ user.py
│        └─ utils.py
├─ Dockerfile
├─ docker-compose.yaml
├─ poetry.lock
├─ pyproject.toml
└─ tox.ini
```

##  Getting Started

```shell script
# Clone the repository
git clone git@github.com:michaeltoohig/charge_points_api.git

# cd into project root
cd charge_points_api

# Launch the project
docker-compose up
```

Afterwards, the project will be live at [http://localhost:5000](http://localhost:5000).

## Documentation

FastAPI automatically generates documentation based on the specification of the endpoints you have written. You can find the docs at [http://localhost:5000/docs](http://localhost:5000/docs).

## Testing

In order to test and lint the project locally you need to install the poetry dependencies outlined in the pyproject.toml file.

If you have Poetry installed then it's as easy as running `poetry shell` to activate the virtual environment first and then `poetry install` to get all the dependencies.

This starter template has an example test which covers its only endpoint. To run the test, ensure you are
in the same directory as the `tox.ini` file and run `tox` from the command line. It will also perform code
linting and formatting as long as the pre-commit hooks were installed. We'll talk about that next.

### Alternative Testing Only

`pytest -s` skips tox and just tests in your local environment

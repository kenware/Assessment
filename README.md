# Assessment
[![Coverage Status](https://coveralls.io/repos/github/kenware/Assessment/badge.svg?branch=develop)](https://coveralls.io/github/kenware/Assessment?branch=develop)
[![CircleCI](https://circleci.com/gh/kenware/Assessment/tree/develop.svg?style=svg)](https://circleci.com/gh/kenware/Assessment/tree/develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/788103f2b045ee5d196f/maintainability)](https://codeclimate.com/github/kenware/Assessment/maintainability)
## Description
Assessment is an open source project built with django restframework API, it is designed to accomodate any form of assessment which include survey, quize, test etc. It support uploading of chart and graphs. in the question and answer objects
Any one can clone this project and customize it for its need.

## Installation Guide
* check that python is installed
    ```bash
    python --V
    ```
* Install Postgres database

* Clone this project
    ```bash
    git clone https://github.com/kenware/Assessment.git
    ```
* Enter project root directory
    ```bash
    cd Assessment
    ```
* install virtual env in your terminal at the project root
    ```bash
    pip install virtualenv
    ```
* Activate virtualenv 
    ```bass
    source .env/bin/activate
    ```
* Install packages
    ```bash
    pip install -r requirements.txt
    ```
* In the root directory, open `env/bin/activate` file and add the environmental variable at the bottom of the `activate` file accordingto the sample bellow:
    ```python
    export DATABASE_NAME=<database_name>
    export DATABASE_USER=<postgres_user>
    export DATABASE_PASSWORD=<postgres password>
    export DATABASE_HOST=localhost
    export DATABASE_PORT=5432
    ```
* Inside the `deactivate` block of code in the `env/bin/activate` file add:
    ```python
    unset DATABASE_NAME
    unset DATABASE_USER
    unset DATABASE_PASSWORD
    unset DATABASE_HOST
    unset DATABASE_PORT
    ```
* The sample activate file can be found on `sample_env_acivate` file in this project.

* Run test
    ```bash
    python manage.py test
    ```
* Migrate tables to postgres database
    ```bash
    python manage.py migrate
    ```
* Add initial data to the database
    ```bash
    python manage.py seed
    ```

* Start the application
    ```bash
    python manage.py runserver
    ```
## Documentation
* This API is fully documented using POSTMAN, however navigate to `basic usage` to get the basic usage of this API

## Basic Usage
### Query Parser Attributes
* All the `GET` all endpoints of the object instance described bellow have the following functionalities:
* Pagination
* Filtering by any valid field on the models. This include filtering by ranges eg `?startCreatedAt=2019-01-05` and `?endCreatedAt=2019-01-19`
* Ordering by ascending or descending order using any valid model field eg `?orderBy=ascId`, `?orderBy=decCreatedAt`
### Assessment Type objects:
* This provides an endpoints that perform all crude operation on assessment objects. To view all endpoint on this, go to the POSTMAN documentation above.
* this object has an attribute `multi-times` which is a boolean. It is `false` by default. If it is set to `true`, users will be allowed to take the same assessment multiple times.
* admin and staffs are allowed to read and write to this enpoints while normal users are allowed to read.

### Questions Object:
* This provides an endpoints that perform all crude operation on question objects. To view all endpoint on this, go to the POSTMAN documentation above.
* This object has an attribute `multi-choice` which is a boolean. It is `false` by default. If it is set to `true`, a questions can a have multiple choice.
* admin and staffs are allowed to read and write to this enpoints
* It surport chart and image

### Answer Object:
* This provides an endpoints that perform all crude operation on answer objects. To view all endpoint on this, go to the POSTMAN documentation above.
* admin and staffs are allowed to read and write to this enpoints
* It surport chart and image

### Assessment Event
* This provides an endpoint that starts an assessment, answer a question and submit an assessment. To view all endpoint on this, go to the POSTMAN documentation above.
* normal users are allowed to read and write to this enpoints

### Score object:
* This holds all the assessment taken by a user and the history of the correct and wrong choices the user made while answering a question.
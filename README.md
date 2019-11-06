# PIZZA API

[![Build Status](https://travis-ci.org/Nta1e/pizza_api.svg?branch=dev)](https://travis-ci.org/Nta1e/pizza_api)
[![Coverage Status](https://coveralls.io/repos/github/Nta1e/pizza_api/badge.svg?branch=dev)](https://coveralls.io/github/Nta1e/pizza_api?branch=dev)

## Description
This is an API for a pizza ordering service built with Django and Django Rest Framework

## The API has the following routes

| METHOD | ROUTE | FUNCTIONALITY |ACCESS|
| ------- | ----- | ------------- | ------------- |
| *POST* | ```/api/signup/``` | _Register new user_| _All users_|
| *POST* | ```/api/login/``` | _Login user_|_All users_|
| *POST* | ```/api/order/``` | _Place an order_|_All users_|
| *PUT* | ```/api/order/update/{order_id}/``` | _Update an order_|_All users_|
| *PUT* | ```/api/order/status/{order_id}/``` | _Update order status_|_Superuser_|
| *DELETE* | ```/api/order/delete/{order_id}/``` | _Delete/Remove an order_ |_All users_|
| *GET* | ```/api/user/orders/``` | _Get user's orders_|_All users_|
| *GET* | ```/api/orders/``` | _List all orders made_|_Superuser_|
| *GET* | ```/api/orders/{order_id}/``` | _Retrieve an order_|_Superuser_|
| *GET* | ```/api/user/order/{order_id}/``` | _Get user's specific order_|_All users_|
| *GET* | ```/api/orders/search/?param=value``` | _Filter orders by status, user's first_name, and user's last_name_|_Superuser_|
| *GET* | ```/docs/``` | _View API documentation_|_All users_|

## PROJECT REQUIREMENTS
- PostgreSQL
- python 3.6 and above
- Docker(If you are to setup with Docker)

## PROJECT SETUP

1. #### Setting up with a Virtual Environment
    - Create a `.env` file in project root following the `.env.example` file
    - Create a `virtual environment` using your preferred method. I'd prefer running
    
        ```bash
         python3 -m venv <env_name>
        ```
    - Activate the virtual environment and install requirements *ie*
    
       ```bash
        pip install -r requirements.txt
       ```
    - Run migrations *ie*
    
        ```bash
         python manage.py migrate
        ```
    - Create a superuser for accessing `admin-only` endpoints with the command
    
       ```bash
        python manage.py createsuperuser
       ```
        
    - Run the server *ie*
    
        ```bash
        python manage.py runserver
        ```
        
2. #### Setting up with Docker
    Before booting up the environment (`make build`) ensure that you have [docker](https://docs.docker.com/) **installed** and **running** on your machine.
    If you are using mac this [install](https://docs.docker.com/docker-for-mac/install/) should get you started.

    The resources will be configured via docker-compose services.
    
    To start the build, run:

    ```bash
    make build
    ```
    After the build is complete, spin up the docker containers with:

    ```bash
    make start
    ```
    Then you can access the application, served by the django development server at `http://localhost:8000`
    
    To stop the application, you can pull down the containers with:

    ```bash
    make stop
    ```
    **NOTE**
        - A superuser is already created for the docker container to access `admin-only` endpoints with the following credentials
        
     ```python
   email = "admin@example.com"
   password = "password123"
      ```
   

## RUNNING TESTS
    
1. To run the tests locally, first ensure that you have a `.env` file which follows the `.env.example` file
   and that you have installed all requirements
    
   Then run the tests with the command:
    ```bash
    coverage run --source=api/ ./manage.py test
    ```
2. To run the tests from within the docker container, run the command `docker ps` to view the available docker containers. Use the command
 
    `docker exec -it [container_id] bash`
    
    Then execute the following command in the bash terminal
    
    ```bash
    coverage run --source=api/ ./manage.py test
    ```
    
    
## Author

*Ntale Shadik*


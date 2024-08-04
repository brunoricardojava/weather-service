# Weather Service

Project developed with the intention of collect weather data.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Config](#config)
- [Running](#running)
- [Testing](#testing)

## Prerequisites

- Docker (https://docs.docker.com/engine/install/)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/brunoricardojava/weather-service.git
    cd drink_water
    ```

## Config

1. Open .env_development and config the project, the default values will run the project.

## Running

1. Start the application container

    ```bash
    docker compose up
    ```

The application will be available at [http://0.0.0.0:5001/](http://0.0.0.0:5001/).

Endpoints:
  [POST] /api/v1/weather/<unique_user_id>
  [GET]  /api/v1/weather/<unique_user_id>

## Testing

1. To run the tests, use:

    ```bash
    docker compose exec web poetry run task test
    ```

2. To check the test coverage, use:

    ```bash
    docker compose exec web poetry run task coverage
    ```

You can access the test coverage report at project-path/htmlcov/index.html

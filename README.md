Surge Pricing
Overview

This project is focused on implementing a surge pricing model, simulating pricing adjustments based on demand 
fluctuations, using Kafka and a Spark cluster for aggregations.
Features

    Dynamic pricing logic: Adjusts prices based on factors such as demand and supply.
    Real-time data processing: Utilizes Python for backend operations.
    Dockerized environment: Easily deployable using Docker.

Setup

    Clone the repository.

git clone https://github.com/denisefavila/surge-pricing.git

Install dependencies:

poetry install

Start the services using Docker Compose:

    docker-compose up --build

Start jobs on Spark Cluster:

    docker-compose up --build

Contributing

    Fork the repository.
    Create a new branch.
    Make your changes and submit a pull request.

License

This project is licensed under the MIT License.


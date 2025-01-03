Surge Pricing
Overview

This project is focused on implementing a surge pricing model, simulating pricing adjustments based on demand 
fluctuations, using Kafka and a Spark cluster for aggregations.

Features
    Driver Position simulator.
    Real time visualization for Drivers Positions and Orders Positions with ElasticSearch + Kibana.
    Dynamic pricing logic: Adjusts prices based on factors such as demand and supply.
    Real-time data processing: Utilizes Python for backend operations.
    Dockerized environment: Easily deployable using Docker.


Driver Positions Real Time Visualization
<img width="1501" alt="Captura de Tela 2025-01-03 às 11 06 47" src="https://github.com/user-attachments/assets/d49c80e4-ea83-4188-b072-f4b58b7252da" />



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


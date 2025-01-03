# Surge Pricing
## Overview

This project focuses on implementing a surge pricing model by simulating pricing adjustments based on demand fluctuations. The solution utilizes Kafka for stream processing and integrates with a Spark cluster for real-time data aggregation. For real-time visualizations and geolocation-based searches, ElasticSearch and Kibana are incorporated, enabling tracking and analysis of driver and order positions. Filebeat is used to collect and ship logs to ElasticSearch. To persist positions, Cassandra is employed as the database, providing high availability and scalability for storing driver and order location data.

## Features

- **Driver Position Simulator**  
  Simulates driver locations in real-time.

- **Positions Real-time Visualization**  
  Displays driver and order positions using **ElasticSearch** and **Kibana**.

  #### Driver Positions Real-Time Visualization
  <div style="text-align: center;">
    <img width="600" alt="Driver Positions Visualization" src="https://github.com/user-attachments/assets/d49c80e4-ea83-4188-b072-f4b58b7252da" />
  </div>


- **Dynamic Pricing Logic**  
  Adjusts prices dynamically based on factors such as demand and supply.

- **Real-time Data Processing**  
  Utilizes **Python** for backend operations.

- **Dockerized Environment**  
  Easily deployable using **Docker**.



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


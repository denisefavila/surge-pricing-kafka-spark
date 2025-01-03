Surge Pricing
## Overview

This project focuses on implementing a surge pricing model by simulating pricing adjustments based on demand fluctuations. The solution uses **Kafka** and a **Spark cluster** for data aggregations.

## Features

- **Driver Position Simulator**  
  Simulates driver locations in real-time.

- **Real-time Visualization**  
  Displays driver and order positions using **ElasticSearch** and **Kibana**.
  Driver Positions Real Time Visualization
  <div style="text-align: center;">
    <img width="600" alt="Captura de Tela 2025-01-03 às 11 06 47" src="https://github.com/user-attachments/assets/d49c80e4-ea83-4188-b072-f4b58b7252da" />
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


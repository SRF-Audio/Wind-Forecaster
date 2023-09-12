# Wind Forecaster

## Overview
Wind Forecaster is a web application designed to fetch and display weather forecast data, with a primary focus on wind conditions for kiteboarders, wind surfers, and wing foilers. It uses a [Flask-based](https://github.com/pallets/flask) Python backend that handles API data retrieval from the [Open-Meteo API](https://open-meteo.com/), and uses [MongoDB](https://www.mongodb.com/) for CRUD operations. On the frontend, it's an [NGINX-based](https://www.nginx.com/) React web app with [Material UI](https://mui.com/material-ui/) for the client side components and interactions. It is containerized and orchestrated using Docker's [`docker compose`](https://docs.docker.com/compose/) for ease of development and testing.

## Getting Started
The project utilizes Docker Compose to orchestrate multiple containers within Docker. This means the frontend, backend and database run in separate containers, but are networked together within Docker, and are also accessible via `localhost`.

### Prerequisites
- [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Install Docker](https://docs.docker.com/desktop/install/mac-install/) and start it
- run `git clone https://github.com/SRF-Audio/Wind-Forecaster.git` in the folder of your choosing
- (Optional, but highly recommended) [Install Mongo Compass](https://www.mongodb.com/products/tools/compass)

### Run with Docker Compose:

Navigate to the project repo's root folder and run:

- `docker-compose up --build` 
(**NOTE**: First time builds may take 2-3 minutes depending on your internet speed. Follow on builds will have cached layers, and should be faster)

Once the build process finishes, the React frontend will be accessible at http://localhost:3000.

11 Sept: If a card shows up on the page with Lat/Long coordinates, then the app is fully working. However, if you'd like to peek under the hood more, then see below.

The Flask backend API can be hit at http://localhost:5000/weather and you should get the JSON response from the DB.

You can also look at the database directly by opening Mongo Compass, and using the connection string: `mongodb://admin:pass@localhost:27017/windForecaster?authSource=admin`
Everything is written to `weather_database` in the `Forecasts` collection.
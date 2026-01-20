# Surf-Spot-Website
The main purpose of this app is to allow a user to create an account and use that to create surf spots and journal their sessions at these spots. Spot creation includes setting ideal conditions and journalling includes the ability to log the conditions of that particular session as well as a place to write up how things went that day. Along with that, non-account holding users can use the site to get the current conditions of NOAA buoys across the world using a map, manually entering in the station number, or finding buoy stations based on your location. 

# Tech Stack
This application follows a typical MVC architecture. React JS is used on the frontend as the View. The Model is the files outside of app.py that perform all logic handling data and interacting with the database. The Controller is the app.py file which contains all the routes that mediate interactions between Model and the frontend. Deployment is handled by containerizing the frontend and backend into two separate images and using docker-compose to orchestrate the services. NGINX is used as a reverse proxy to serve the React frontend and route client requests to the Flask backend. SSL/TLS certificates for HTTPS is handled using Certbot and mounted to the frontend container via Docker volumes.

# Database Design
<img width="699" alt="Screenshot 2024-05-26 at 2 51 17 PM" src="https://github.com/jsperling23/Surf-Spot-Website/assets/95095370/9a162cbc-3da1-4a62-8db6-1d10e14456dd">



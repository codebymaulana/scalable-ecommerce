Microservices E-commerce Platform
This project is a scalable e-commerce platform built on a microservices architecture using FastAPI. It separates core business functions into independent services, which allows for easier development, maintenance, and scaling.

<br>

🚀 Services
Each service is a self-contained FastAPI application

1. User Service
This service is responsible for all user-related functions. It manages user data, authentication, and security.

2. Product Catalog Service
This service manages the product inventory and related data.

3. Shopping Cart Service
This service handles the logic for a user's shopping cart.


4. Order Service
This service manages the complete order lifecycle, from creation to historical tracking.

5. Payment Service
This service securely handles payment processing and integration with external gateways.

6. Notification Service
This service sends real-time notifications via email and SMS for key events. It uses a message broker like Kafka to process these tasks asynchronously.

7. Frontend
This service using vue.js act for client interaction in the e-commerce web app
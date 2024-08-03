# syntax=docker/dockerfile:1

# Frontend Build
FROM node:20.11.0-alpine as build-step
WORKDIR /frontend

ENV PATH /frontend/node_modules/bin:$PATH
COPY package.json package-lock.json ./
COPY . .
RUN npm install
RUN npm run build

# NGINX Build
FROM nginx:stable-alpine
COPY --from=build-step /frontend/build /usr/share/nginx/html
COPY /deployment/nginx.conf /etc/nginx/nginx.conf

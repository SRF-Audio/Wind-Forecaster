# Stage 1: Build the React application
FROM node:14 AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the local files to the container's workspace.
COPY . ./

# Build the React app
RUN npm run build

# Stage 2: Serve the React application from Nginx server
FROM nginx:alpine

# Copy the build output from stage 1
COPY --from=build /app/build /usr/share/nginx/html

# Use a basic nginx configuration
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for the nginx server
EXPOSE 80

# Command to run when the container starts
CMD ["nginx", "-g", "daemon off;"]

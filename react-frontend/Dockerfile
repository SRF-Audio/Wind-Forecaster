# Use Node 14 image
FROM node:14

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the local files to the container's workspace.
COPY . ./

# Expose the default port for Create React App (3000)
EXPOSE 3000

# Start the React development server
CMD ["npm", "start"]

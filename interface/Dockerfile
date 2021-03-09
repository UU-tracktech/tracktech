FROM node AS builder 
COPY react react
WORKDIR /react
RUN ["npm","run","build"]

# Created by WebStorm
FROM node:15 AS runner
RUN npm install -g serve

# Open the port
EXPOSE 5000

# copy static files
COPY testconfig.json /config.json 
COPY entrypoint.sh /entrypoint.sh

# Copy the build program
COPY --from=builder /react/build /build

# Set the entrypoint to the script
ENTRYPOINT ["/entrypoint.sh"]
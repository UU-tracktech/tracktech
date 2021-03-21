FROM node:15 AS builder
COPY react react
WORKDIR /react
RUN ["npm","run","build"]

# Created by WebStorm
FROM node:15 AS runner
RUN npm install -g serve

# Open the port
EXPOSE 5000

# copy static files
COPY testconfig.json /build/config.json

# Copy the build program
COPY --from=builder /react/build /build


ENTRYPOINT ["serve", "-s", "build"]
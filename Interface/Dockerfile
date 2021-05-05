FROM node:15 AS builder
WORKDIR /react
COPY react/package.json ./package.json
COPY react/package-lock.json ./package-lock.json
RUN ["npm","install"]
COPY react/tsconfig.json ./tsconfig.json
COPY react/craco.config.js ./craco.config.js
COPY react/.prettierrc.json ./.prettierrc.json
COPY react/public ./public
COPY react/src ./src
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
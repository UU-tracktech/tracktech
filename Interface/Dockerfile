FROM node:15 as installer
WORKDIR /react
COPY react/package.json ./package.json
COPY react/package-lock.json ./package-lock.json
RUN ["npm","install"]


FROM installer as source
WORKDIR /react
COPY react/public ./public
COPY react/src ./src


FROM source AS builder
WORKDIR /react
COPY react/tsconfig.json ./tsconfig.json
COPY react/craco.config.js ./craco.config.js
COPY react/.prettierrc.json ./.prettierrc.json
RUN ["npm","run","build"]

# linting
FROM source AS linter
WORKDIR /react

COPY react/.eslintrc.json ./.eslintrc.json
COPY react/.prettierrc.json ./.prettierrc.json
COPY react/testing ./testing

ENTRYPOINT ["./node_modules/.bin/eslint", "src/**/*.tsx", "src/**/*.ts", "src/**/*.tsx"]


FROM source AS testing
WORKDIR /react
COPY react/babel.config.json ./babel.config.json
COPY react/jest.config.js ./jest.config.js
COPY react/tsconfig.json ./tsconfig.json
COPY react/styleMock.js ./styleMock.js
COPY react/setupJest.js ./setupJest.js


FROM testing AS unit-testing
WORKDIR /react

COPY ["react/testing/unit testing","./testing/unit testing"]

ENTRYPOINT ["npm", "test", "--", "--coverage", "testing/unit testing"]


FROM testing AS integration-testing
WORKDIR /react

COPY ["react/testing/integration testing","./testing/integration testing"]

ENTRYPOINT ["npm", "test", "--", "--coverage", "testing/integration testing"]



# Created by WebStorm
FROM node:15 AS production
RUN npm install -g serve

# Open the port
EXPOSE 5000

# Copy the build program
COPY --from=builder /react/build /build

ENTRYPOINT ["serve", "-s", "build"]

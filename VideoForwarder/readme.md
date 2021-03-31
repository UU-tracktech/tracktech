# run
```
docker-compose up --build
```

# Environment
## General
* CONFIG_PATH: The path to the configuration file containing stream informatio

## Streaming
* SEGMENT_SIZE: The size of a single segment in seconds (default 1)
* SEGMENT_AMOUNT: The amount of segments stored at once for a single stream (default 5)
* REMOVE_DELAY: The amount of seconds of inactivity before a stream is closed (default 60)
* TIMEOUT_DELAY: The amount of seconds to wait for a stream to open and produce segments (default 30)

## SSL
Must both be specified in order to use SSL
* SSL_CERT: The ssl certificate path
* SSL_KEY: The ssl key path

## Authentication
* PUBLIC_SECRET: The public key file to validate the tokens with
* TOKEN_AUDIENCE: The if of this client
* TOKEN_SCOPE: The scope to check for in the token
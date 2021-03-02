# Created by WebStorm
FROM node:15
RUN npm install -g serve

WORKDIR /tmp/project_modules
EXPOSE 5000

COPY build /tmp/project_modules/build/
CMD ["serve", "-s", "build"]
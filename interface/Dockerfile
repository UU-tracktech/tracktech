# Created by WebStorm
FROM node:15
WORKDIR /tmp/project_modules
COPY package.json /tmp/project_modules/package.json
COPY public /tmp/project_modules/public/
COPY src /tmp/project_modules/src/
RUN npm install .
COPY start.sh /tmp/project_modules/start.sh
EXPOSE 8080
CMD ["node", "app.tsk"]
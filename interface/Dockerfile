# Created by WebStorm
FROM node:15
WORKDIR /tmp/project_modules
#COPY package.json /tmp/project_modules/package.json
#COPY public /tmp/project_modules/public/
#COPY src /tmp/project_modules/src/
#RUN npm install .
#COPY start.sh /tmp/project_modules/start.sh
#EXPOSE 8080
#CMD ["node", "app.tsk"]



#FROM ubuntu

#MAINTAINER Luke Crooks "luke@pumalo.org"

# Update aptitude with new repo
RUN apt-get update

# Install software
RUN apt-get install -y git
# Make ssh dir
RUN mkdir /root/.ssh/

# Copy over private key, and set permissions
# Warning! Anyone who gets their hands on this image will be able
# to retrieve this private key file from the corresponding image layer
ADD deployment_rsa /root/.ssh/deployment_rsa

# Create known_hosts
RUN touch /root/.ssh/known_hosts
# Add bitbuckets key
RUN ssh-keyscan -T 30 git.science.uu.nl >> /root/.ssh/known_hosts

# Clone the conf files into the docker container
RUN git clone -b SCP_63-TEST-BRANCH --single-branch git@git.science.uu.nl:e.w.j.bangma/tracktech/interface/src.git /tmp/project_modules/ && \
    git clone -b SCP_63-TEST-BRANCH --single-branch git@git.science.uu.nl:e.w.j.bangma/tracktech/interface/public.git /tmp/project_modules/ && \
    git clone -b SCP_63-TEST-BRANCH --single-branch git@git.science.uu.nl:e.w.j.bangma/tracktech/interface/start.sh.git /tmp/project_modules/ && \
    git clone -b SCP_63-TEST-BRANCH --single-branch git@git.science.uu.nl:e.w.j.bangma/tracktech/interface/package.json.git /tmp/project_modules/

COPY start.sh /tmp/project_modules/start.sh

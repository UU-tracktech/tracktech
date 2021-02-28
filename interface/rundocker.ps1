echo "git-user:x:$(id -u):$(id -g):Git User:/tmp:/bin/bash" > /tmp/fake_passwd # See below why to use this
docker run \
   -u $(id -u):$(id -g) \
   -w /tmp/project_modules \
   -v $HOME/.ssh/id_rsa \
   -v /tmp/fake_passwd:/etc/passwd  \
   --entrypoint sh \
   -it \
   alpine/git

# commands in the container:
$ export GIT_SSH_COMMAND='ssh -i $HOME/.ssh/id_rsa -o "StrictHostKeyChecking=no"'
$ git clone git@git.science.uu.nl:e.w.j.bangma/tracktech.git
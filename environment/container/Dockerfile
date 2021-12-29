# Set the base image
FROM python:3

# Set environment variables
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# COPY, best pratices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
RUN mkdir /usr/src/app
COPY ./ ./usr/src/app
RUN cd usr/src/app && ls -la

# Update and
RUN apt-get update && apt-get -yq dist-upgrade

# Installs
RUN apt-get install -y git \
                       vim \
                       tree \
                       wget \
    && pip install --no-cache-dir -r usr/src/app/src/environment/requirements.txt

# Clean
RUN apt autoclean  \
    && rm -rf /var/lib/apt/lists/*

# Set config jupyter
RUN mkdir $HOME/.jupyter/
RUN mv usr/src/app/src/environment/jupyter_notebook_config.py $HOME/.jupyter/

# Set working directory
WORKDIR /usr/src/app

# Run shell command for notebook on start
CMD jupyter notebook --ip 0.0.0.0 --no-browser --allow-root

# Set the base image
FROM python:3.11-slim

# Set environment variables
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN mkdir -p /usr/src/app
COPY ./ /usr/src/app/

# Update and install system packages
RUN apt-get update && apt-get -yq dist-upgrade \
    && apt-get install -y --no-install-recommends \
       git \
       vim \
       tree \
       wget \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

# NOTE: Add a requirements.txt to the project root and uncomment the line below:
# RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# Set up Jupyter configuration
RUN mkdir -p $HOME/.jupyter/ \
    && cp /usr/src/app/environment/jupyter_notebook_config.py $HOME/.jupyter/

# Set working directory
WORKDIR /usr/src/app

# Run shell command for notebook on start
CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--no-browser", "--allow-root"]

# get OS
FROM ubuntu:22.04

# update OS
RUN apt-get update

# get additional packages
RUN apt-get install -y --no-install-recommends \
    gcc \
    git \
    time \
    zlib1g-dev \
    libjpeg-dev \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel

# clone fsqc
#RUN git clone --branch dev --single-branch https://github.com/Deep-MI/fsqc.git /app/fsqc
RUN git clone https://github.com/Deep-MI/fsqc.git /app/fsqc

# install additional python packages (TODO: not necessary if using pip install)
RUN pip3 install -r /app/fsqc/requirements.txt

# Add other environment variables
ENV OMP_NUM_THREADS=1
ENV MPLCONFIGDIR=/tmp/mplconfigdir

# Set the working directory to /app
WORKDIR /app

# Set entrypoint (non-interactive mode)
ENTRYPOINT ["python3", "/app/fsqc/run_fsqc"]

## Run app when the container launches (interactive mode)
#CMD ["/bin/bash"] 


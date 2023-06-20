# get OS
FROM ubuntu:22.04

# update OS
RUN apt-get update

# get additional packages
RUN apt-get install -y --no-install-recommends \
     git \
     zlib1g-dev \
     libjpeg-dev \
     time \
     python3 \
     python3-dev \
     python3-pip \
     python3-setuptools \
     python3-wheel

# clone qatools-python
RUN git clone https://github.com/Deep-MI/qatools-python.git /app/qatools-python

# install additional python packages
RUN pip3 install -r /app/qatools-python/requirements.txt

# Add other environment variables
ENV OMP_NUM_THREADS=1

# Set the working directory to /app
WORKDIR /app

# Set entrypoint (non-interactive mode)
ENTRYPOINT ["python3", "/app/qatools-python/qatools.py"]

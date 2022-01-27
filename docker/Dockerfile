# get OS
FROM ubuntu:18.04

# update OS
RUN apt-get update

# get additional packages
RUN apt-get install -y --no-install-recommends \
     ca-certificates \
     wget \
     tar \
     zip \
     man \
     git \
     gcc \
     tcsh \
     zlib1g-dev \
     libjpeg-dev \
     time \
     python3 \
     python3-dev \
     python3-pip \
     python3-setuptools \
     python3-wheel

# download FreeSurfer
RUN wget -qO- https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/6.0.1/freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.1.tar.gz | tar zxv --no-same-owner -C /opt \
    --exclude='freesurfer/trctrain' \
    --exclude='freesurfer/subjects/fsaverage_sym' \
    --exclude='freesurfer/subjects/fsaverage3' \
    --exclude='freesurfer/subjects/fsaverage4' \
    --exclude='freesurfer/subjects/fsaverage5' \
    --exclude='freesurfer/subjects/fsaverage6' \
    --exclude='freesurfer/subjects/cvs_avg35' \
    --exclude='freesurfer/subjects/cvs_avg35_inMNI152' \
    --exclude='freesurfer/subjects/V1_average' \
    --exclude='freesurfer/average/mult-comp-cor' \
    --exclude='freesurfer/lib/cuda' \
    --exclude='freesurfer/lib/qt'\
    --exclude='freesurfer/MCRv80'

# clone qatool-spython, brainprint-python, and lapy toolboxes
RUN git clone https://github.com/Deep-MI/LaPy.git /app/lapy
RUN git clone https://github.com/Deep-MI/BrainPrint-python.git /app/brainprint
RUN git clone https://github.com/Deep-MI/qatools-python.git /app/qatools-python

# install additional python packages
#RUN pip3 install -r /app/qatools-python/requirements.txt
RUN pip3 install `cat /app/qatools-python/requirements.txt | grep -v "importlib" | grep -v "#.*" `

# Add FreeSurfer environment variables (.license file needed, alternatively export FS_LICENSE=path/to/license)
ENV FREESURFER_HOME=/opt/freesurfer

# Add other environment variables
ENV OMP_NUM_THREADS=1

# Set the PATH
ENV PATH=/opt/freesurfer/bin:/opt/freesurfer/fsfast/bin:/opt/freesurfer/tktools:/opt/freesurfer/mni/bin:${PATH}

# Add toolbox directories to PYTHONPATH
ENV PYTHONPATH=/app/lapy:/app/brainprint:${PYTHONPATH}

# Set the working directory to /app
WORKDIR /app

# Set entrypoint (non-interactive mode)
ENTRYPOINT ["python3", "/app/qatools-python/qatools.py"]

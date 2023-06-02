# QATools Docker

Here we provide a [`Dockerfile`](Dockerfile) that can be used to create a Docker image and subsequently run the qatools scripts within a Docker container.

The docker image will be based on Ubuntu, contain the qatools scripts, the lapy and brainprint libraries, and any additionally required packages from the Ubuntu distribution.

## Build qatools Docker image

To build the docker image, execute the following command after traversing into the *docker* directory of this repository:

```bash
docker build --rm -t qatoolsdocker -f Dockerfile .
```
The name of the image will be `qatoolsdocker`, and it will be built from the `Dockerfile` configuration file from the *docker* directory.

The `--rm` flag will remove intermediate containers after a successful build; `-t` specifies the name of the image, and `-f` indicates the configuration file from which to build.

Take a look at the contents of the [`Dockerfile`](Dockerfile) to see what is done during the build process: essentially, it is getting the Ubuntu 18.04 image, installing additional packages from the distribution, downloading the qatools-python, brainprint-python, and lapy toolboxes, and setting the necessary environment variables. Unless the `Dockerfile` changes, the build process has to be done only once.

## Run qatools from a Docker image

After building the qatoolsdocker image, run it with the following command to see the help message of the qatools-python main script:

```bash
docker run --rm --user XXXX:YYYY qatoolsdocker
```

* This corresponds to calling `python3 qatools.py` from the command line for a non-dockerized version of the program.
* The `--rm` flag takes care of removing the container once the analysis finished.
* The `--user XXXX:YYYY` part should be changed to the appropriate user id (XXXX, a number) and group id (YYYY, also a number); both can be checked with the commands `id -u` and `id -g` on linux-like systems). All generated files will then belong to the specified user and group. Without the flag, the docker container will be run as root with all corresponding privileges, which is strongly discouraged.

An actual analysis can be performed by adding several options to the above command (and after adjusting the user-specific settings and file- and pathnames):

```bash
docker run \
    --rm \
    --user XXXX:YYYY \
    -v /path/to/my/subjects/directory:/path_to_subjects_directory_inside_docker \
    -v /path/to/my/output/directory:/path_to_output_directory_inside_docker \
    qatoolsdocker \
    --subjects_dir /path_to_subjects_directory_inside_docker \
    --output_dir /path_to_output_directory_inside_docker
```

* The first two `-v` arguments mount your data directory and output directories into the docker image. Inside the image, they are visible under the name following the colon (in this case `/data` and `/output`, but these can be different). From within the docker image / container, there will be read and write access to the directories that are mounted into the image (unless specified otherwise).
* The next part of the docker command is the name of the Docker image, which is `qatoolsdocker`.
* After that, all other flags are identical to the ones that are used for the `qatools.py` program (which are explained on the main page and the help message of the program). In addition to the `--subjects_dir` and `--output_dir` arguments, which are mandatory, the `--subjects`, `-screenshots`, `--fornix` arguments, for example, could be specified - in the same way as for non-dockerized version of the program. Note that file- and pathnames need to correspond to the targets of the file / directory mappings within the Docker image, not to the local system.
* Also note that if you supply additional filenames to the qatools script (using e.g. the `--subjects-file` argument), their locations must be mounted using another `-v` option (unless they are present in one of the already mounted directories), and the filenames given to the script need to refer to the mounted location inside the Docker.

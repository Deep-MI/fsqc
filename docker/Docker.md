# QATools Docker 

Here we provide a `Dockerfile` that can be used to create a Docker image and subsequently run the qatools scripts within a Docker container.

The docker image will be based on Ubuntu 18.04, contain a Freesurfer 6.0 installation, the qatools scripts, the lapy and brainprint libraries, and any additionally required packages from the Ubuntu distribution. 

The only thing that is required to run the qatools pipeline with all options, is a valid FreeSurfer license (either from your local FreeSurfer installation or from the FreeSurfer website; https://surfer.nmr.mgh.harvard.edu/registration.html). 

## Build qatools Docker image

To build the docker image, execute the following command after traversing into the *docker* directory of this repository: 

```bash
docker build --rm -t qatoolsdocker -f Dockerfile .
```

The name of the image will be `qatoolsdocker`, and it wil be built from the `Dockerfile` configuration file from the *docker* directory. 

The `--rm` flag will remove intermediate containers after a successful build; `-t` specifies the name of the image, and `-f` indicates the configuration file from which to build. 

Take a look at the contents of the [`Dockerfile`](Dockerfile) to see what is done during the build process: essentially, it is getting the Ubuntu 18.04 image, installing additional packages from the distribution, downloading and installing a copy of FreeSurfer 6.0 (without some of the very large image files and directories, which are not needed), downloading the qatools-python, brainprint-python, and lapy toolboxes, and setting the necessary environment variables. The result image will have a size of approximately 7 GB.

## Run qatools from a Docker image

After building the qatoolsdocker image, run it with the following command to see the help message of the qatools-python main script:

```bash
docker run --rm --user XXXX:YYYY qatoolsdocker
```

* The --rm flag takes care of removing the container once the analysis finished. 
* The --user XXXX:YYYY part should be changed to the appropriate user id (XXXX, a number) and group id (YYYY, also a number); both can be checked with the commands `id -u` and `id -g` on linux systems). All generated files will then belong to the specified user and group. Without the flag, the docker container will be run as root with all corresponding privileges, which is strongly discouraged.

An actual analysis can be performed by adding several options (and after adjusting the user-specific settings and file- and pathnames):

```bash
docker run \
    --rm \
    --user XXXX:YYYY \
    -v /path/to/my/subjects/directory:/path_to_subjects_directory_inside_docker \
    -v /path/to/my/output/directory:/path_to_output_directory_inside_docker \
    -v /path/to/my/freesurfer/license/file:/opt/freesurfer/.license:ro \
    qatoolsdocker \
    --subjects_dir /path_to_subjects_directory_inside_docker \
    --output_dir /path_to_output_directory_inside_docker
```

* The first two `-v` commands mount your data directory and output directory into the docker image. Inside it is visible under the name following the colon (in this case `/data` and `/output`, but these can be different). From within the docker image / container, there will be read and write access to the directories that are mounted into the image (unless specified otherwise).
* The third `-v` command mount your local FreeSurfer license file into the FreeSurfer directory within the docker image (`/opt/freesurfer`). The `:ro` suffix indicates that from within Docker, this will be read-only.
* The command next mentions the name of the Docker image, which is `qatoolsdocker`. After that, all other flags are identical to the ones that are used for the `qatools.py` (which are explained on the main page or the help message). In addition to the `--subjects_dir` and `--output_dir` arguments, which are mandatory, the `--subjects`, `-screenshots`, `--fornix` arguments, among others, can be specified. This is just the same as for non-dockerized version of the program. Note that file- and pathnames need to correspond to the targets of the file / directory mappings within the Docker image, not to the local system. 



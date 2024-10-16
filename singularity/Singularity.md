# Singularity

We host releases of the fsqc package as Docker images on [Dockerhub](https://hub.docker.com/r/deepmi/fsqcdocker/tags). For use on HPC systems or in other cases where Docker is not preferred you can easily create a Singularity image from the Docker images. 

## Creating s Singularity image
For creating a singularity image from the Dockerhub just run: 

```bash
cd /home/user/my_singlarity_images
singularity build fsqc-latest.sif docker://deepmi/fsqcdocker:latest
```

Singularity Images are saved as `.sif` files. Here the _/home/user/my_singlarity_images_ is the path where you want your file saved. You can change _deepmi/fsqc:latest_ with any tag provided in our [Dockerhub](https://hub.docker.com/r/deepmi/fsqcdocker/tags).

If you want to use a locally available image that you created yourself, instead run:

```bash
cd /home/user/my_singlarity_images
singularity build fsqc-myimage.sif docker-daemon://fsqc:myimage
```

For how to create your own Docker images see our [Docker guide](../docker/Docker.md)

## Using a Singularity image

```bash
singularity exec \
    -B /path/to/subjects/directory:/data \
    -B /path/to/subjects/directory:/out \
    /home/user/my_singularity_images/fsqc-myimage.sif \
    /app/fsqc/run_fsqc \
    --subjects_dir /data \
    --output_dir /out
```

* The first two `-B` arguments mount your data directory and output directories into the singularity image (note that full, not relative, pathnames should be given). Inside the image, they are visible under the name following the colon (in this case `/path_to_filename_inside_container` and `/path_to_output_directory_inside_container`, but these can be different). From within the singularity image / container, there will be read and write access to the directories that are mounted into the image (unless specified otherwise).
* The next part of the command is the name of the Singularity image, which is `fsqc-myimage.sif` in this example, but can be freely chosen depending on what was set during the build process (see above). In this example, the image is located in `/home/user/my_singularity_images`, but the specific path will likely be different on your local system.
* For the Singularity image, we also have to explicitly specify the command that we want run, i.e. `python3 /app/fsqc/run_fsqc`.
* After that, all other flags are identical to the ones that are used for the `fsqc` program (which are explained on the main page and the help message of the program). That is, there can be more options than specified in this example command. Note that file- and pathnames need to correspond to the targets of the file / directory mappings within the singularity image, not to the local system.

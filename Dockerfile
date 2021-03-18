FROM continuumio/miniconda:latest
 
WORKDIR /app
 
COPY ./environment.yml ./
 
RUN conda env create -f environment.yml -n my_env
 
# ENV PATH /opt/conda/envs/my_env/bin:$PATH
 
# RUN /bin/bash -c "source activate my_env"

COPY ./ ./

# RUN ["conda", "activate", "my_env"]
# RUN conda install -n my_env --file environment.yml
# RUN ["conda", "install", "-c", "conda-forge", "opencv"]
# RUN ["apt-get", "update"]
# RUN ["apt-get", "install", "-y", "cmake"]
# RUN ["apt", "install", "-y", "libopencv-dev"]
# RUN ["apt", "install", "-y", "python-opencv"]
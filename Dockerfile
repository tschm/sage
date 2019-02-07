# Set the base image to beakerx
FROM sagemath/sagemath:latest

# set the user back to root to install further packages
#USER root

# copy over the requirements file (links to our private github repositories)
#COPY requirements.txt requirements.txt

#RUN pip install --no-cache-dir --upgrade pip

# copy over the config file (contains the hashed password)
COPY ./jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py

# install our packages (which subsequently link to sqlalchemy, etc.)
#RUN pip install --no-cache-dir  --target "/opt/conda/envs/beakerx/lib/python3.6/site-packages" -r requirements.txt && rm requirements.txt

# set the user back to NB_USER defined in Dockerfile for beakerx/beakerx
#USER $NB_USER

EXPOSE 8888
CMD sage-jupyter
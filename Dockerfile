# Set the base image to beakerx
FROM sagemath/sagemath:latest

# copy over the config file (contains the hashed password)
COPY ./jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py

RUN pip install pandas

EXPOSE 8888
CMD sage-jupyter
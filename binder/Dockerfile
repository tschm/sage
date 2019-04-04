# Set the base image to beakerx
FROM sagemath/sagemath:8.7

# Copy the Notebooks into the image
COPY ./work ${HOME}/work

# Copy the package into the image and install
COPY . /tmp/sage
RUN sage -pip install --no-cache-dir /tmp/sage line-profiler

EXPOSE 8888

CMD sage-jupyter
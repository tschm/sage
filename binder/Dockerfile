# Set the base image to beakerx
FROM sagemath/sagemath:8.6

COPY ./books ${HOME}/books

RUN sage -pip install --no-cache-dir pandas

EXPOSE 8888
CMD sage-jupyter
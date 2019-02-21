# Set the base image to beakerx
FROM sagemath/sagemath:8.6

COPY ./books ${HOME}/work
RUN echo ${HOME}/work

RUN sage -pip install --no-cache-dir pandas==0.24.1 line-profiler

EXPOSE 8888

CMD sage-jupyter
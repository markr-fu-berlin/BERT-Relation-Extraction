
#FROM registry.datexis.com/bwinter/datexis-pytorch:python3.7-cuda10.1

FROM python:3.6-slim

#RUN python -m pip install --upgrade pip

RUN pip install --upgrade pip

COPY ./requirements.txt /home/
RUN pip install -r  /home/requirements.txt


COPY ./src  /home/src
COPY ./main_task.py  /home/

#RUN mkdir /home/data
COPY ./data /home/data

COPY ./Entrypoint.sh  /home/
RUN chmod +x  /home/Entrypoint.sh

RUN python -m spacy download en_core_web_lg

WORKDIR /home

ARG MAKE_TASTY_MODEL

ENV ENV_MAKE_TASTY_MODEL=$MAKE_TASTY_MODEL

CMD ["/bin/sh", "-c", "sleep 5d"]
#ENTRYPOINT "/workspace/Entrypoint.sh" $ENV_MAKE_TASTY_MODEL $ENV_DATA_PATH $ENV_TASTY_MODEL_NAME $ENV_FORCE_NEW $ENV_ENCODER_MODEL $ENV_MODEL_START
















#FROM registry.datexis.com/bwinter/datexis-pytorch:python3.7-cuda10.1

FROM python:3.6-slim

#RUN python -m pip install --upgrade pip

RUN pip install --upgrade pip

COPY ./requirements.txt /home/
RUN pip install -r  /home/requirements.txt

RUN python -m spacy download en_core_web_lg

COPY ./data /home/data
COPY ./model /home/model

COPY ./src  /home/src
COPY ./main_task.py  /home/

COPY ./Entrypoint.sh  /home/
RUN chmod +x  /home/Entrypoint.sh

WORKDIR /home

# these are equivalent to the arguments in Parser.py
ARG train_data
ARG test_data
ARG train
ARG infer
ARG model_path

ENV ENV_train_data=$train_data
ENV ENV_test_data=$test_data
ENV ENV_train=$train
ENV ENV_infer=$infer
ENV ENV_model_path=$model_path


#CMD ["/bin/sh", "-c", "sleep 5d"]
ENTRYPOINT "/home/Entrypoint.sh" $ENV_train $ENV_infer $ENV_model_path $ENV_train_data $ENV_test_data















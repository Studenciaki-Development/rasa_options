FROM rasa/rasa:1.10.11-full
WORKDIR /app

USER root
RUN pip install fuzzywuzzy

COPY ./custom_nlu /app/custom_nlu
COPY ./data/lookup_table.json /app/data

USER 1001

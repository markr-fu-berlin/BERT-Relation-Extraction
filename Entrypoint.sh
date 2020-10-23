#!/bin/sh

python -m spacy download en_core_web_lg #( into ~/data/  /home/data, check if exists)
exec python main_task.py --model_no 0 --model_size 'bert-base-uncased' --infer 1 --train 1
exec
exit

/fsmount/mkress/BERT-rel-ex


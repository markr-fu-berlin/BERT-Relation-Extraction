#!/bin/sh

# $ENV_train_data $1
# $ENV_test_data $2
# $ENV_train $3
# $ENV_infer $4
# $ENV_model_path $5


if [ $1 = "" ]; then
  if [ $2 = "" ]; then
    echo no test- and train-datapath given
    exec python main_task.py  --train $3 --infer $4 --model_path $5
  fi
else
  echo test- and train-datapath given
  exec python main_task.py  --train $3 --infer $4 --model_path $5 --test_data $2 --train_data $1
fi

exit



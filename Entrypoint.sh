#!/bin/sh


# $ENV_train $1
# $ENV_infer $2
# $ENV_model_path $3
# $ENV_train_data $4
# $ENV_test_data $5


echo ENV_train_data $4
echo ENV_test_data $5
echo ENV_train $1
echo ENV_infer $2
echo ENV_model_path $3




if [ -z "$4" ]; then
  if [ -z "$5" ]; then
    echo no test- and train-datapath given
    exec python main_task.py  --train $1 --infer $2 --model_path $3
  fi
else
  echo test- and train-datapath given
  exec python main_task.py  --train $1 --infer $2 --model_path $3 --test_data $5 --train_data $4
fi

exit



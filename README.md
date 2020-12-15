# BERT(S) for Relation Extraction

## Overview
Adaptation of https://github.com/plkmo/BERT-Relation-Extraction to run as a Kubernetes/Flask-Service for inferring Entity-Relations on given sentences.


## Requirements
 
Pre-trained BERT models (ALBERT, BERT) courtesy of HuggingFace.co (https://huggingface.co)   
Pre-trained BioBERT model courtesy of https://github.com/dmis-lab/biobert   
SemEval2010 Task 8 dataset, available [here.](https://github.com/sahitya0000/Relation-Classification/blob/master/corpus/SemEval2010_task8_all_data.zip)

To use BioBERT(biobert_v1.1_pubmed), download & unzip the [contents](https://drive.google.com/file/d/1zKTBqqrCGlclb3zgBGGpq_70Fx-qFpiU/view?usp=sharing) to ./additional_models folder.   


## Training by matching the blanks (BERT<sub>EM</sub> + MTB)

Not explicitly supported by this adaption, but it should be easy to do with a few changes.
See oroginal README to see how to run main_pretraining.py .

## Fine-tuning on SemEval2010 Task 8 (BERT<sub>EM</sub>/BERT<sub>EM</sub> + MTB)

Download the SemEval2010 Task 8 dataset(or your dataset of choice with same format) and unzip to "./data/" folder.
You could also unzip to your bound volume and set the --train_data and --test_data arguments.

Build the dockerfile.

If you need to train your model first, build with --train 1, --infer 1, and set --model_path to a path to save the model to.
if you have a trained model, build with --model_path <path>, --train 0 --infer 1.

```bash
docker build -t <registry-name> --build-arg train=0 --build-arg infer=1 --build-arg model_path=<your modelpath> .
docker push <registry-name>
```
--train_data and test_data are optional, but if one is set the other has to be set as well.

```bash
docker build -t <registry-name> --build-arg train=0 --build-arg infer=1 --build-arg model_path=<your modelpath --build-arg train_data=<traindata_path> --build-arg test_data=<testdata_path> .
docker push <registry-name>
```

Then push to your registry.

Start the kubernetes deployment and service.
```bash
kubectl create -f RelEx.yaml 
kubectl create -f RelExService.yaml 
```

The frontend for this Service can be found here: https://github.com/markr-fu-berlin/HRLRE-flask-api-front/tree/BERT-RelEx



This Service will automatically detect potential entities in an input sentence, and return the entity-pair with the highest corresponding relation-prediction.
If you want to add the possibility to find relation-prediction for predetermined entities you need to switch

```python
inferer.infer_sentence(test, detect_entities=False)
```
to 
 ```python
inferer.infer_sentence(test, detect_entities=True)
```
and inpute the senteces marked like this:

```bash
The surprise [E1]visit[/E1] caused a [E2]frenzy[/E2] on the already chaotic trading floor.
```

This service outputs the sentences and annotation in texoo-format, but split into sentences. If there are multiple annotations for the same sentence, the sentence will be returned multiple times. If this needs changing, change the "get_all_predictions" method in main_task.py accordingly.

There is the option to input sentences in texoo-format, but there is currently no way to do this with the frontend. Also every input-sentence needs its own entry in the "data"-list of the input.

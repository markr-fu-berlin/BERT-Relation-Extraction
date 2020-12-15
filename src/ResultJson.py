import logging
import json
import re
import copy

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', \
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger('__file__')


def new_annotation(document_ref, confidence, rel_args):
    annotation = {
                    "length": None,
                    "documentRef": document_ref,
                    "uid": None,
                    "text": None,
                    "begin": None,
                    "classs": "relationAnnotation",
                    "type": None,
                    "source": None,
                    "confidence": confidence,
                    "isActive": False,
                    "predicate": "Example Relation Predicate",
                    "relationArguments": [
                        {
                            "length": rel_args[0][1],
                            "documentRef": document_ref,
                            "uid": None,
                            "text": rel_args[0][0],
                            "begin": rel_args[0][2],
                            "classs": "relationArgument",
                            "type": "GENERIC",
                            "source": None,
                            "confidence": None,
                            "isActive": False
                        },
                        {
                            "length": rel_args[1][1],
                            "documentRef": document_ref,
                            "uid": None,
                            "text": rel_args[1][0],
                            "begin": rel_args[1][2],
                            "classs": "relationArgument",
                            "type": "GENERIC",
                            "source": None,
                            "confidence": None,
                            "isActive": False
                        }
                    ]
                }

    return annotation


def jsonline(length, document_ref, uID, text, begin, thisClass, type, source, confidence, rel_args):
    document_ref = 1
    begin = 0

    annotation = new_annotation(document_ref, confidence, rel_args)

    line = {'length': length,
            'documentRef': document_ref,
            'uid': uID,
            'text': text,
            'begin': begin,
            'class': thisClass,                                     #relation type zb mention_annotaion,
            'type': type,
            "tokens": None,
            "empty": None,
            "language":  None,
            "sentences":  None,
            'source': source,
            'id': None,
            "title": "Output for bert-relex-api.demo.datexis.com",

            "annotations": [
                annotation
            ]
           }

    return line



def find_E1_E2(sentence):
    split_on_E1 = sentence.split("[E1]")
    if "[/E1]" in split_on_E1[0]:
        E1, residual = split_on_E1[0].split("[/E1]")
        sentence = ' '.join([residual, split_on_E1[1]])
    elif "[/E1]" in split_on_E1[1]:
        E1, residual = split_on_E1[1].split("[/E1]")
        sentence = ' '.join([split_on_E1[0], residual])
    else:
        logger.info("overlapping entities not caught")
        return None, None

    split_on_E2 = sentence.split("[E2]")
    if "[/E2]" in split_on_E2[0]:
        E2, _ = split_on_E2[0].split("[/E2]")
    elif "[/E2]" in split_on_E2[1]:
        E2, _ = split_on_E2[1].split("[/E2]")
    else:
        logger.info("overlapping entities not caught")
        return None, None
    return E1, E2


def get_annotations(sentence, sentext):
    if "[E1]" in sentence and "[E2]" in sentence:
        E1, E2 = find_E1_E2(sentence)
        if E1 is None or E2 is None:
            return [None, None, None], [None, None, None]

        E1_start = len(sentext.split(E1)[0])
        E2_start = len(sentext.split(E2)[0])

        # if the punctuation is part of the entities there are problems, so remove them.
        if E1_start > len(E1):
            E1_start = len(sentext.split(E1[:-2])[0])
        if E2_start > len(E2):
            E2_start = len(sentext.split(E2[:-2])[0])

        return [E1, len(E1), E1_start],\
                [E2, len(E2), E2_start]
    else:
        return [None,None,None], [None,None,None]



def make_result_json_from_simple(data):
    # {"data":[
    #    {"sentext": "original sentence",
    #     "sentence": "anotated sentece",
    #     "pred": "class name",
    #     "prob": 0.087
    #     }
    # ]}
    jsonlines = []
    for line in data:
        length = len(line["sentext"])
        text = line["sentext"]
        thisClass = line["pred"]
        confidence = line["prob"]
        rel_args = get_annotations(line["sentence"], line["sentext"])

        document_ref = None
        begin = None
        type = None
        source = None
        uID = None

        json_line = jsonline(length, document_ref, uID, text, begin, thisClass, type, source, confidence, rel_args)
        jsonlines.append(json_line)

    return '{"data":' + json.dumps(jsonlines) + '}'

def make_result_json_from_texoo(data):
    logger.info("make_res full : " + str(data) + "\n")
    new_data = []
    for line in data:
        newline = copy.deepcopy(line)
        logger.info("make_res : " + str(newline) + "\n")
        rel_args = get_annotations(newline["sentence"], newline["text"])
        annotation = new_annotation(newline["documentRef"], newline["prob"], rel_args)
        newline["thisClass"] = newline["pred"]
        newline["annotations"].append(annotation)
    #
        newline.pop("sentence")
        newline.pop("pred")
        newline.pop("prob")
        new_data.append(newline)

    return json.dumps(new_data)

def make_result_json(data, inputtype = "simplejson"):
    if inputtype == "simplejson":
        jsonObj = make_result_json_from_simple(data)

    elif inputtype == "texoo":
        jsonObj = make_result_json_from_texoo(data)

    return jsonObj
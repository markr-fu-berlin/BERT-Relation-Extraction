#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 17:40:16 2019

@author: weetee
"""
from src.tasks.trainer import train_and_fit
from src.tasks.infer import infer_from_trained, FewRel
from src.Parser import Parser
from src.ResultJson import make_result_json
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
import sys
import logging
import json
from operator import itemgetter

# TODO change README of frontend
# TODO return options?
# TODO add options to frontend
# TODO put all annotations in one texoo?
# TODO texoo input better?
# tODO remove cases where entitys are switched?


'''
This fine-tunes the BERT model on SemEval, FewRel tasks
'''

logging.basicConfig(filename="/home/RelEx.log", format='%(asctime)s [%(levelname)s]: %(message)s', \
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger(__name__)

def make_app(argv, debug=False):
    app = Flask(__name__)
    #CORS(app, support_credentials=True)
    # TODO
    # @cross_origin(supports_credentials=True)
    # def login():
    #    return jsonify({'success': 'ok'})
    app.debug = debug

    parser = Parser().getParser()
    #argv = sys.argv[1:]
    args, _ = parser.parse_known_args()
    
   # args = parser.parse_args()
    
    if (args.train == 1) and (args.task != 'fewrel'):
        app.net = train_and_fit(args)

    if (args.infer == 1) and (args.task != 'fewrel'):
        app.inferer = infer_from_trained(args.model_path, detect_entities=True, args=args)

    if args.task == 'fewrel':
        fewrel = FewRel(args.model_path, args)
        meta_input, e1_e2_start, meta_labels, outputs = fewrel.evaluate()

    def find_best_prediction(out):
        best_pred = max(out, key=itemgetter(2))
        return best_pred[0], best_pred[1], best_pred[2]

    def get_best_predictions(data, inputtype="simplejson"):
        if inputtype == "simplejson":
            sen_name = "sentext"
        elif inputtype == "texoo":
            sen_name = "text"

        for line in data:
            #logger.info("sentence"+ str(line[sen_name]))
            out = app.inferer.infer_sentence(line[sen_name], detect_entities=True)
            logger.info("out: " + str(out))
            line["sentence"], line["pred"], line["prob"] = find_best_prediction(out)
        return data

    def get_all_predictions(data, inputtype="simplejson"):
        new_data = []
        if inputtype == "simplejson":
            sen_name = "sentext"
        elif inputtype == "texoo":
            sen_name = "text"

        for line in data:
            logger.info("sentence" + str(line[sen_name]))
            out = app.inferer.infer_sentence(line[sen_name], detect_entities=True)
            logger.info("out: " + str(out))

            if len(out) == 0:
                logger.info("test")
                line["sentence"], line["pred"], line["prob"] = None, None, None
                new_data.append(line)
            else:
                for pred in out:
                    logger.info("pred : " + str(pred))
                    newline = line
                    newline["sentence"], newline["pred"], newline["prob"] = pred[0], pred[1], pred[2]
                    new_data.append(newline)
        return new_data


    # takes new texoo json for each line
    # ignores annotations and generates new ones
    @app.route('/api/importtexoo', methods=['POST'])
    def get_input_importtexoo():
        print("request.data: ", request.data)
        logger.info("request.data:" + str(request.data))

        #jsonInput = request.get_json(force=True)
        jsonInput = { "options": {"returnAllPredictions": True},
                    "data": [
                        {'length': 12,
                        'documentRef': 2,
                        'uid': 123,
                        'text': "I  love  Easter Sunday as a fashion moment because every church goer is ready to praise while dressed to the nines in their best Spring-inspired looks .",
                        'begin': 0,
                        'class': "thisClass",
                        'type': "type",
                        "tokens": None,
                        "empty": None,
                        "language": "ENg",
                        "sentences": None,
                        'source': "source",
                        'id': None,
                        "title": "Output for bert-relex-api.demo.datexis.com",

                        "annotations": [
                            {"relationArguments": [
                                {"arg1": "blq"},{"arg2": "ble"}]},
                            {"relationArguments": [
                                {"arg1": "blj"}, {"arg2": "blg"}]}
                            ]
                        }
                    ]
                 }

        jsonInput = json.loads(jsonInput)

        if jsonInput["options"]["returnAllPredictions"]:
            data = get_all_predictions(jsonInput["data"], "texoo")
        else:
            data = get_best_predictions(jsonInput["data"], "texoo")

        return make_result_json(data, "texoo")


    @app.route('/api/importjson', methods=['POST'])
    def get_input_importjson():
        print("request.data: ", request.data)
        logger.info("request.data:" + str(request.data))


        #jsonInput = request.get_json(force=True)
        jsonInput = '{ "options": {"returnAllPredictions": true},' \
                    '"data": [' \
                    '{"sentext": "I  love  Easter Sunday as a fashion moment because every church goer is ready to praise while dressed to the nines in their best Spring-inspired looks ."},' \
                   ' {"sentext": "Wear  them with basics and sparse accessories ."}' \
                    ']}'
        jsonInput = json.loads(jsonInput)

        if jsonInput["options"]["returnAllPredictions"]:
            data = get_all_predictions(jsonInput["data"])
        else:
            data = get_best_predictions(jsonInput["data"])

        return make_result_json(data)

    return app


if __name__ == '__main__':
    argv = sys.argv[1:]
    app = make_app(argv, debug=False)
    app.run(host='0.0.0.0')

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
from operator import itemgetter

#TODO set data-folder / model-folder from parameters


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
    logger.info("logger working")
    app.debug = debug

    parser = Parser().getParser()
    #argv = sys.argv[1:]
    args, _ = parser.parse_known_args()
    
   # args = parser.parse_args()
    
    if (args.train == 1) and (args.task != 'fewrel'):
        app.net = train_and_fit(args)

    if (args.infer == 1) and (args.task != 'fewrel'):
        app.inferer = infer_from_trained(args, detect_entities=True)

    if args.task == 'fewrel':
        fewrel = FewRel(args)
        meta_input, e1_e2_start, meta_labels, outputs = fewrel.evaluate()

    def find_best_prediction(out):
        #[[sent, pred, prob],[sent, pred, prob]]
        best_pred = max(out, key=itemgetter(2))
        return best_pred[0], best_pred[1], best_pred[2]


    @app.route('/api/importjson', methods=['POST'])
    def get_input_importjson():
        print("request.data: ", request.data)
        logger.info("request.data:" + str(request.data))

        jsonInput = request.get_json(force=True)

        for line in jsonInput["data"]:  # TODO make parallel? if yes need id

            #logger.info("sentence"+ str(line["sentext"]))
            out = app.inferer.infer_sentence(line["sentext"], detect_entities=True)
            logger.info("out: " + str(out))
            line["sentence"], line["pred"], line["prob"] = find_best_prediction(out)

        json = make_result_json(jsonInput)
        return json

    return app


if __name__ == '__main__':
    argv = sys.argv[1:]

    app = make_app(argv, debug=False)
    app.run(host='0.0.0.0')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 17:40:16 2019

@author: weetee
"""
from src.tasks.trainer import train_and_fit
from src.tasks.infer import infer_from_trained, FewRel
from src.Parser import Parser
import logging

#TODO set data-folder / model-folder from parameters
#TODO python -m spacy download en_core_web_lg #( into ~/data/  /home/data, check if exists), curretly in fsmount
#TODO make flask ap
#TODO start without exec
#TODO ask about en_core_web_lg https://spacy.io/models/en#en_core_web_lg
#TODO test infer
#TODO make speak texoo
# TODO get probabilirys

'''
This fine-tunes the BERT model on SemEval, FewRel tasks
'''

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', \
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger('__file__')

if __name__ == "__main__":
    parser = Parser().getParser()
    #argv = sys.argv[1:]
    args, _ = parser.parse_known_args()
    
   # args = parser.parse_args()
    
    if (args.train == 1) and (args.task != 'fewrel'):
        net = train_and_fit(args)
        
    if (args.infer == 1) and (args.task != 'fewrel'):
        inferer = infer_from_trained(args, detect_entities=True)

        test = "The surprise [E1]visit[/E1] caused a [E2]frenzy[/E2] on the already chaotic trading floor."
        out = inferer.infer_sentence(test, detect_entities=False)
        print("out: ", out)
        test2 = "After eating the chicken, he developed a sore throat the next morning."
        out = inferer.infer_sentence(test2, detect_entities=True)
        print("out: ", out)


        while True:
            sent = input("Type input sentence ('quit' or 'exit' to terminate):\n")
            if sent.lower() in ['quit', 'exit']:
                break
            out = inferer.infer_sentence(sent, detect_entities=True)
            print("out: ", out)
    
    if args.task == 'fewrel':
        fewrel = FewRel(args)
        meta_input, e1_e2_start, meta_labels, outputs = fewrel.evaluate()
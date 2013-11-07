#!/bin/bash

PARENTDIR=/Users/joelc/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/

# go to the mallet directory
cd ${PARENTDIR}openideo-data-processing-pipeline/semantic-models/mallet-2.0.7

NUMTOPICS=300
INPUT=${PARENTDIR}SemanticModelData/mallet/inputs/openIDEO_CF1_DF50.mallet
OUTPUT_KEYS=${PARENTDIR}SemanticModelData/mallet/outputs/openideo_CF1_DF50_${NUMTOPICS}_ASP_optim_keys.txt
OUTPUT_DOCS=${PARENTDIR}SemanticModelData/mallet/outputs/openideo_CF1_DF50_${NUMTOPICS}_ASP_optim_composition.txt

# train the topic model
./bin/mallet train-topics --input $INPUT --num-topics $NUMTOPICS --output-topic-keys $OUTPUT_KEYS --output-doc-topics $OUTPUT_DOCS --use-symmetric-alpha false --show-topics-interval 100 --optimize-interval 10

# reshape the output
cd ${PARENTDIR}openideo-data-processing-pipeline/model-post-processing

OUTPUT_DOCS_RESHAPED=${PARENTDIR}/SemanticModelData/mallet/outputs/sorted_openideo_CF1_DF50_${NUMTOPICS}_ASP_optim_composition.csv

python reshape_mallet_doctopiccomposition.py $OUTPUT_DOCS $OUTPUT_DOCS_RESHAPED $NUMTOPICS
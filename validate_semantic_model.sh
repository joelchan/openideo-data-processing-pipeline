#!/bin/bash

PARENTDIR=/Users/joelc/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/
NUMTOPICS=(12 20 30 40 50 60 70 80 90 100 150 200 300 400 500)
INPUT=${PARENTDIR}SemanticModelData/mallet/inputs/openIDEO_CF1_DF50.mallet

for NUMTOPIC in "${NUMTOPICS[@]}"
do
    
    # make the names
    OUTPUT_KEYS=${PARENTDIR}SemanticModelData/mallet/outputs/openideo_CF1_DF50_${NUMTOPIC}_ASP_optim_keys.txt
    OUTPUT_DOCS=${PARENTDIR}SemanticModelData/mallet/outputs/openideo_CF1_DF50_${NUMTOPIC}_ASP_optim_composition.txt
    
    # train the topic model
    cd ${PARENTDIR}openideo-data-processing-pipeline/semantic-models/mallet-2.0.7
    ./bin/mallet train-topics --input $INPUT --num-topics $NUMTOPIC --output-topic-keys $OUTPUT_KEYS --output-doc-topics $OUTPUT_DOCS --use-symmetric-alpha false --show-topics-interval 100 --optimize-interval 10
    
    # reshape the output
    cd ${PARENTDIR}openideo-data-processing-pipeline/model-post-processing
    OUTPUT_DOCS_RESHAPED=${PARENTDIR}/Validation/LDA_CF1_DF50_ASP_opt10/sorted_openideo_CF1_DF50_${NUMTOPIC}_ASP_optim_composition.csv
    python reshape_mallet_doctopiccomposition.py $OUTPUT_DOCS $OUTPUT_DOCS_RESHAPED $NUMTOPIC

done


#Probably better to do something like this:
#
#for numtopic in NUMTOPIC:
#    train model
#    save output to directory
#    
#benchmark_continuous # will iterate over the output files in the directory
    

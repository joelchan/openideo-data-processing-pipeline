#!/bin/bash

PARENTDIR=/Users/joelc/Desktop/Dropbox/Research/Dissertation/OpenIDEO/Pipeline/
OUTPUTDIR=/Users/joelc/Desktop/LDA_CF1_DF50_ASP_90_opt10/

NUMTOPICS=(12 25 50 100 150 200 300 400 500 600 700)
INPUT=${PARENTDIR}SemanticModelData/mallet/inputs/openIDEO_CF1_DF50.mallet

for NUMTOPIC in "${NUMTOPICS[@]}"
do
    
    RUNS=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50)
    
    for RUN in "${RUNS[@]}"
    do
    
        # make the names
        OUTPUT_KEYS=${OUTPUTDIR}RawOutputs/CF1_DF50_${NUMTOPIC}_ASP_optim_keys-${RUN}.txt
        OUTPUT_DOCS=${OUTPUTDIR}RawOutputs/CF1_DF50_${NUMTOPIC}_ASP_optim_composition-${RUN}.txt
        OUTPUT_STATE=${OUTPUTDIR}RawOutputs/CF1_DF50_${NUMTOPIC}_ASP_optim_topic-state-${RUN}.gz
            
        # train the topic model
        cd ${PARENTDIR}openideo-data-processing-pipeline/semantic-models/mallet-2.0.7
        ./bin/mallet train-topics --input $INPUT --num-topics $NUMTOPIC --output-topic-keys $OUTPUT_KEYS --output-doc-topics $OUTPUT_DOCS --output-state $OUTPUT_STATE --use-symmetric-alpha false --show-topics-interval 100 --optimize-interval 10
            
        # reshape the output
        cd ${PARENTDIR}openideo-data-processing-pipeline/model-post-processing
        OUTPUT_DOCS_RESHAPED=${OUTPUTDIR}ForValidation/sorted_CF1_DF50_${NUMTOPIC}_ASP_optim_composition-${RUN}.csv
        python reshape_mallet_doctopiccomposition.py $OUTPUT_DOCS $OUTPUT_DOCS_RESHAPED $NUMTOPIC
    
    done

done
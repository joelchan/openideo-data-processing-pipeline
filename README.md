openideo-data-processing-pipeline
=================================

This folder holds all the code that I'm currently using to either pre-process or post-process data, 
and some code for "data collection" (e.g., downloading HTML files, extracting comments, genealogies, etc.).
I'm still working out the details for the structure of the pipeline, but the code here handles:
- extracting genealogies from pairwise citation data
- extracting comments from HTML files
- tokenization of text
- feature selection and input file preparation for semantic models
- searching the feature space (using gensim) for LSA and LDA
- similarity queries for semantic models
- some random R code for post-processing and exploring the data

More to come...


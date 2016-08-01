# Phenotype prediction tool based on IRIS-Plex model

 Main code is "model_test.py". It is implemented for iris pigmentation prediction based on vcf data according to the mathematical model provided in [Susan Walsh et al. 2010 paper](http://s3.amazonaws.com/academia.edu.documents/44985285/IrisPlex_A_sensitive_DNA_tool_for_accura20160422-9059-1ka4psb.pdf?AWSAccessKeyId=AKIAJ56TQJRTWSMTNPEA&Expires=1469612124&Signature=3ya4xQdBzyKHqXTleumD5GorB%2F4%3D&response-content-disposition=inline%3B%20filename%3DIrisPlex_A_sensitive_DNA_tool_for_accura.pdf)

## Testing the code
Primarily, you need to start test_func_model.py and test.py. They are to be started from the root.
 If that works correctly, you then need to proceed to your own data

## Usage
 The code is to be started from the root repository "digital_phenotyping/" in the following way:

 
     model-test/model_test.py -m eye -v /complete/path/to/the/vcf_file.vcf -s on -p /complete/path/to/model/arguments/folder/

 It requires 2 arguments:

 -m or --mode is a mode of analysis -- you need to select the phenotypical trait analyzed (eye / hair or skin pigmentation are available, in this version -- eye only). 

 -v or --vcf is a complete path to the vcf file sample

 There are two auxillary arguments:

 -s or --silent is an argument to print out the analysis on the screen it is OFF by default, to see the output you need to set it to ON

 -p or --param is a full path to the parameters (such as model coefficients etc), can be set by user. By default a folder in the repository is set, as it contains the parameters for Iris Plex.

## Obtaining the self-reported phenotype

 Self-reported phenotype data can be obtained via the following [questionnaire](https://goo.gl/forms/A9cJcRTU1QlXESFu1). It is required to download the results in the tab-separated values format or .tsv.
 
 Self-reported phenotype is obtained via poll-parser.py:


     model-test/poll_parser.py -p /complete/path/to/the/poll/answers.tsv -s sample_name

 It requires 2 arguments:

 -p or --poll is a complete path to the tsv file with phenotype self-reports

 -s or --sample is the name of the sample

## Validating the model

 Validation of the model is comparison of the model estimation output with the self-reported phenotype. Currently only Iris Plex validation is available. 

 Basically, it combines both of the scripts mentioned above and has interpreting set of functions and comparing set. The script to be implemented is validator.py


     model-test/validator.py -m eye -v /complete/path/to/the/folder_with_vcfs -p /complete/path/to/model/arguments/folder/ -c /complete/path/to/the/poll/answers.tsv -s sample_name

 The arguments mentioned here are the combination of the arguments used above. 


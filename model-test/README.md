># Phenotype prediction tool based on IRIS-Plex model.
>
> Main code is "model_test.py". It is implemented for iris pigmentation prediction based on vcf data according to the mathematical model provided in [Susan Walsh et al. 2010 paper](http://s3.amazonaws.com/academia.edu.documents/44985285/IrisPlex_A_sensitive_DNA_tool_for_accura20160422-9059-1ka4psb.pdf?AWSAccessKeyId=AKIAJ56TQJRTWSMTNPEA&Expires=1469612124&Signature=3ya4xQdBzyKHqXTleumD5GorB%2F4%3D&response-content-disposition=inline%3B%20filename%3DIrisPlex_A_sensitive_DNA_tool_for_accura.pdf)
>
>## Testing the code.
>Primarily, you need to start test_func_model.py and test.py
> If that works correctly, you then need to proceed to your own data
>
>## Usage
> model_test.py requires 2 arguments:
> -m or --mode is a mode of analysis -- you need to select the phenotypical trait analyzed (eye / hair or skin pigmentation are available, in this version -- eye only). 
> -v or --vcf is a complete path to the vcf file sample
> *TO BE ADDED* -c or --check option -- that compares model output with self-report -- complete path to the questionnaire of phenotypic traits.

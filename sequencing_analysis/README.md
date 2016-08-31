#Statistical model selection for SNPs analysis
1) Available tools description
2) Models used

## Tools for SNPs, indels -based analysis

###HIrisPlex
The tool is available (here)[http://hirisplex.erasmusmc.nl]. Input file is csv like this:
`sampleid,rs12913832_T,rs1800407_A,rs12896399_T,rs16891982_C,rs1393350_T,rs12203592_T`
Output -- either for hair or for eye color -- is a list of phenotypes and their probabilities. Sum of probabilities is 1.

### Snipper
The tool is available (here)[http://mathgene.usc.es/snipper/index.php]. It is rather a cohort-classifier than a phenotype predictor. Input is xsl file or manual input with selection of number of populations, volume of populations, SNP/indel names and SNP values.
Output -- result page with several tables, showing percentage of cohort-specific SNPs/indels. Thus, might be used for analysis with prescribed cohorts for particular phenotypic traits.
In case of skin tone analysis input is nucleotides string in certain order which stands for SNP values.
(Skin tone can be analyzed here).[http://mathgene.usc.es/snipper/skinclassifier.html]
## Prediction models
In (Fan Liu et al., 2009)[http://www.sciencedirect.com/science/article/pii/S0960982209005971] publication five models are compared:
1) Ordinal regression
2) Multinomial logistic regression
3) Fuzzy c-means clustering
4) Neural networks 
5) Classification tree

It is said, that MLR has shown the best results, thus, it was chosen for further analysis and implemented in Irisplex. In hair color analysis: red color was omitted, blond-brown-black were predicted the same way. Red was predicted according to MC1R cumulative mutation.  

Three other possible approaches are:
1) STRUCTURE algorithm
2) PCA
3) Bayesian classification system (used in Snipper) 

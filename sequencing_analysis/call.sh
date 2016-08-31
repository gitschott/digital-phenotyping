#!/bin/bash/sh

docker pull parseq/tsvc:4.4.3
docker run --rm parseq/tsvc:4.4.3

~/bedtools2/bin/intersectBed -a IAD68442_172_Submitted_SNPs.bed -b IAD68442_172_Phenotype_v1.1_Designed.bed > res.bed

echo "let the analysis begin"

docker run --rm \
    -v /Users/apple/vcf/vcyo:/mnt/tsvc-output \
    -v /Users/apple/vcf/alignment_res:/mnt/input_bam \
    -v /Users/apple/vcf/hg19_aln:/mnt/reference \
    -v /Users/apple/vcf:/mnt/parameters \
    parseq/tsvc:4.4.3 variant_caller_pipeline.py\
        --input-bam       /mnt/input_bam/R_2014_03_04_14_44_06_Sequoia_SN1-50-AmpliSeq_SNP-HID-L_P_27.01.15.IonXpress_001.bam \
        --reference-fasta /mnt/reference/hg19_aln.fasta \
        --primer-trim-bed /mnt/parameters/res.bed \
        --parameters-file /mnt/parameters/ampliseq_germline_lowstringency_pgm_parameters.json \
        --output-dir      /mnt/tsvc-output

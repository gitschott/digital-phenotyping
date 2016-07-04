#!/bin/bash

echo "let the analysis begin"

cd ~/data/alignment_results/folder_with_indexed_bam/
for f in *.bam
do
  echo "$f is being analyzed"
  docker run --rm \
      -v /Users/apple/vcf/$f:/mnt/tsvc-output \
      -v /Users/apple/vcf:/mnt/hospo \
      -v /Users/apple/vcf/data/alignment_results:/mnt/input_bam \
      -v /Users/apple/vcf/references/hg19_aln:/mnt/reference \
      -v /Users/apple/vcf/references:/mnt/parameters \
    parseq/tsvc:4.4.3 variant_caller_pipeline.py\
          --hotspot-vcf     /mnt/hospo/hotspots.vcf \
          --input-bam       /mnt/input_bam/$f \
          --reference-fasta /mnt/reference/hg19_aln.fasta \
          --region-bed      /mnt/parameters/de.bed \
          --parameters-file /mnt/parameters/ampliseq_germline_lowstringency_pgm_parameters.json \
          --output-dir      /mnt/tsvc-output


  echo "completed $f"

done



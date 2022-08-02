# ManeCheck

Script checks a VEP annotated VCF file (product of running a vcf through VEP with the MANE option selected) to count the number of variants from that VCF that appear in a MANE transcript.

Add the verbose flag to get a printout of the results dictionary (one entry per vcf record)



Example output:

###############################################################
Total records: 90, No. MANE Select: 88, No. MANE Clinical: 86
###############################################################
Variants below are not associated with any MANE transcript:
Record(CHROM=7, POS=140739814, REF=G, ALT=[C])
###############################################################
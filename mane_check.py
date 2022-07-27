import vcf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--vcf', required=True,
    help=(
        'filename of VCF (VEP annotated with MANE option).'
        )
    )
args = parser.parse_args()


vcf_reader = vcf.Reader(open(args.vcf, 'r'))

record_count = 0
mane_select_count = 0
mane_clinical_count = 0
results = {}

for record in vcf_reader:
    record_count = record_count + 1
    info = record.INFO
    ensembl_id = []
    mane_select = []
    mane_clinical = []
    # get all the transcript IDs from the list of consequences
    for transcript in info['CSQ']:
        if transcript.split('|')[23] != '':
            ensembl_id.append(transcript.split('|')[6])
            mane_select.append(transcript.split('|')[23])
        if transcript.split('|')[24] != '':
            ensembl_id.append(transcript.split('|')[6])
            mane_clinical.append(transcript.split('|')[24])
    
    unique_mane_select = set(mane_select)
    unique_mane_clinical = set(mane_clinical)

    if unique_mane_select:
        mane_select_count = mane_select_count + 1
    if unique_mane_clinical:
        mane_clinical_count = mane_clinical_count + 1

    results[str(record)] = {'ensembl_ids': set(ensembl_id), 'mane_select_ids':unique_mane_select, 'mane_clinical_ids':unique_mane_clinical}


print(f'###############################################################\nTotal records: {record_count}, No. MANE Select: {mane_select_count}, No. MANE Clinical: {mane_clinical_count}\n###############################################################')

for key, value in results.items():
    print(key, '\t', value)

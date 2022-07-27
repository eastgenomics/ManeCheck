import vcf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--vcf', required=True,
    help=(
        'filename of VCF (VEP annotated with MANE option).'
        )
    )
parser.add_argument(
    '--verbose', action='store_true',
    help=(
        'if selected, prints the results in dictionary form for every \
            variant in the input file.'
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

    results[str(record)] = {'ensembl_ids': set(ensembl_id),
                            'mane_select_ids': unique_mane_select,
                            'mane_clinical_ids': unique_mane_clinical}

sep = '###############################################################'

print(
    f'{sep}\nTotal records: {record_count}, \
No. MANE Select: {mane_select_count}, \
No. MANE Clinical: {mane_clinical_count}\n{sep}'
)

if args.verbose:
    for key, value in results.items():
        print(key, '\t', value)

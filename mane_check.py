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

with open(args.vcf, 'r') as infile:
    vcf_reader = vcf.Reader(infile)

    record_count = 0
    mane_select_count = 0
    mane_clinical_count = 0
    results = {}
    lacking_both = []

    info_str = vcf_reader.infos
    format_str = info_str['CSQ'].desc.split('Format: ')[1]
    format_list = format_str.split('|')

    csq_dict = {}
    for i, j in enumerate(format_list):
        csq_dict[j] = i

    for record in vcf_reader:
        record_count = record_count + 1
        info = record.INFO
        ensembl_id = []
        mane_select = []
        mane_clinical = []
        # get all the transcript IDs from the list of consequences
        for transcript in info['CSQ']:
            if transcript.split('|')[csq_dict['MANE_SELECT']] != '':
                ensembl_id.append(transcript.split('|')[csq_dict['Feature']])
                mane_select.append(transcript.split('|')[csq_dict['MANE_SELECT']])
            if transcript.split('|')[csq_dict['MANE_PLUS_CLINICAL']] != '':
                ensembl_id.append(transcript.split('|')[csq_dict['Feature']])
                mane_clinical.append(transcript.split('|')[csq_dict['MANE_PLUS_CLINICAL']])
        
        unique_mane_select = set(mane_select)
        unique_mane_clinical = set(mane_clinical)

        if not unique_mane_select and not unique_mane_clinical:
            lacking_both.append(str(record))

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
No. MANE Clinical: {mane_clinical_count}\n{sep}\n\
Variants below are not associated with any MANE transcript:'
)

for i in lacking_both:
    print(i)

print(sep)

if args.verbose:
    for key, value in results.items():
        print(key, '\t', value)

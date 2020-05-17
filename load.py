import shlex, subprocess

demo_tables = [
    'DEMO',
]

diet_tables = [
    'DR1IFF',
    'DR2IFF',
    'DR1TOT',
    'DR2TOT',
    'DRXFCD',
    'DS1IDS',
    'DS2IDS',
    'DS1TOT',
    'DS2TOT',
    'DSQIDS',
    'DSQTOT',
]

exam_tables = [
    'AUX',
    'AUXAR',
    'AUXTYM',
    'AUXWBR',
    'BPX',
    'BMX',
    'DXX',
    'FLXCLN',
    'OHXDEN',
    'OHXREF'
]

lab_tables = [
    'AMDGYD',
    'ALB_CR',
    'APOB',
    'UADM',
    'UTAS',
    'UTASS',
    'BFRPOL',
    'CHLMDA',
    'HDL',
    'TRIGLY',
    'TCHOL',
    'CRCO',
    'CBC',
    'CUSEZN',
    'COT',
    'UCOT',
    'UCOTS',
    'DEET',
    'SSDEET',
    'ETHOX',
    'FASTQX',
    'FERTIN',
    'FLDEP',
    'FLDEW',
    'FOLATE',
    'FOLFMS',
    'FORMAL',
    'GHB',
    'HEPA',
    'HEPBD',
    'HEPB_S',
    'HEPC',
    'HEPE',
    'HSV',
    'HSCRP',
    'HIV',
    'ORHPV',
    'HPVP',
    'HPVSWC',
    'HPVSWR',
    'SSNEON',
    'INS',
    'UIO',
    'PBCD',
    'UHG',
    'IHGEM',
    'UM',
    'UMS',
    'SSMHHT',
    'PCBPOL',
    'OGTT',
    'PERNT',
    'PERNTS',
    'PFAS',
    'EPHPP',
    'PSTPOL',
    'PHTHTE',
    'GLU',
    'POOLTF',
    'UCPREG',
    'TST',
    'UAS',
    'UASS',
    'BIOPRO',
    'TFR',
    'TRICH',
    'UCFLOW',
    'UVOC',
    'UVOCS',
    'VOCWB',
    'VOCWBS'
]

questionnaire_tables = [
    'ACQ',
    'ALQ',
    'AUQ',
    'BPQ',
    'CDQ',
    'CBQ',
    'HSQ',
    'DEQ',
    'DIQ',
    'DBQ',
    'DLQ',
    'DUQ',
    'ECQ',
    'FSQ',
    'HIQ',
    'HEQ',
    'HUQ',
    'HOQ',
    'IMQ',
    'INQ',
    'KIQ_U',
    'MCQ',
    'DPQ',
    'OCQ',
    'OHQ',
    'PUQMEC',
    'PAQ',
    'PFQ',
    'RXQ_RX',
    'RXQASA',
    'RHQ',
    'SXQ',
    'SLQ',
    'SMQ',
    'SMQFAM',
    'SMQRTU',
    'SMQSHS',
    'VTQ',
    'WHQ',
    'WHQMEC'
]

TEMP_DIR = "tmp/"
def process_tables(year_start, year_end, postfix, tables):
    for table in tables:
        print("Processing Table: " + table)
        with open(TEMP_DIR + table + ".XPT", "w") as file:
            subprocess.run(["curl", "https://wwwn.cdc.gov/Nchs/Nhanes/"+ year_start + "-" + year_end + "/" + table + "_" + postfix + ".XPT"], stdout=file, check=True)
        result = {}
        with open(TEMP_DIR + table + ".CSV", "w") as file:
            result = subprocess.run(["python", "-m", "xport", TEMP_DIR + table +  ".XPT"], stdout=file)
        if result.returncode == 0:
            subprocess.run(["bq", "rm", "-f", "nhanes-277516:NHANES_" + year_start + "_" + year_end + "." + table + "_" + postfix ], stdout=subprocess.PIPE)
            subprocess.run(["bq", "load", "--replace", "--source_format=CSV", "--autodetect", "--project_id=nhanes-277516", "NHANES_" + year_start + "_" + year_end + "." + table, TEMP_DIR + table + ".CSV"], stdout=subprocess.PIPE, check=True)
        else:
            print("Skipping " + table)

process_tables("2013", "2014", "H", demo_tables)
process_tables("2013", "2014", "H", diet_tables)
process_tables("2013", "2014", "H", exam_tables)
process_tables("2013", "2014", "H", lab_tables)
process_tables("2013", "2014", "H", questionnaire_tables)

process_tables("2015", "2016", "I", demo_tables)
process_tables("2015", "2016", "I", diet_tables)
process_tables("2015", "2016", "I", exam_tables)
process_tables("2015", "2016", "I", lab_tables)
process_tables("2015", "2016", "I", questionnaire_tables)
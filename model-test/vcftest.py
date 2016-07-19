import os

def parse_vcf(vcf):
    strings = []
    for file in os.listdir(os.path.abspath(vcf)):
        path = os.getcwd()
        os.chdir(vcf)
        vicief = open(file, 'r', encoding='cp1252')
        for q, line in enumerate(vicief):
            # exclude comment lines
            if line.startswith('#'):
                pass
            else:
                # analyse only actual informative lines
                if line.startswith('chr'):
                    string = str.split(line, sep='\t')
                    print(string)
                    for s in string:
                        # select rs of interest
                        so = s[0]
                        if so.startswith('rs'):
                            fl = [file, line]
                            strings.append(fl)
        os.chdir(path)

    return strings
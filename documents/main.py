"""
Court Calendar 
"""

HEADER_END = '*' * 20

FingerPrint = '********'


class RptHeader:
    def __init__(self):
        self.rundate = None
        self.location = None

class Defendent:
    def __init__(self, fileid, name, complaintant, attorney):
        self.fileid = fileid
        self.name = name
        self.complainant = complaintant
        self.attorney = attorney

class Case:
    def _init__(self, m_or_f, crime, fingerprint):
        self.m_or_f = m_or_f
        self.crime = crime
        self.fingerprint = fingerprint


def is_page_header(line):
    return (line[0] == '1') and ("RUN DATE:" not in line)

def is_report_header(line):
    return (line[0] != '1') and ("RUN DATE:" in line)

def is_summary_header(line):
    return (line[0] == '1') and ("RUN DATE:" in line)

def read_header(infile):
    while True:
        line = infile.readline()
        if HEADER_END in line:
            break

def read_report_header(infile, line):
    hdr = RptHeader()
    hdr.rundate = line[12:20]

    while True:
        line = infile.readline()
        if HEADER_END in line:
            break
    
    return hdr

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

filename = r"DISTRICT.DISTRICT_COURT_.11.12.19.AM.9999.CAL.txt"
rpt_hdr = None

infile = open(filename)
data = None
while True:
    line = infile.readline()

    if line == '\n':
        continue
    elif is_summary_header(line) or line == "":
        break
    elif is_page_header(line):
        read_header(infile)
    elif is_report_header(line):
        rpt_hdr = read_header(infile)
    else:
        '''print(line.split())'''
        data = line.split()
        '''print len(data)'''
        if (len(data) > 0 and is_number(data[0])) == True:
            print([data[2],data[3],data[4],data[6]])
        ''' if FingerPrint in line'''




'''print(temp)'''
'''print(data[2])'''
'''list.append ( Defendent(data[2],data[3],data[4], data[6]) )
print(len(list))'''
'''for obj in list: 
print(obj.fileid, obj.name, obj.complainant, obj.attorney)'''
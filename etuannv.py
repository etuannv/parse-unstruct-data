#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

__author__ = ["Tuan Nguyen"]
__copyright__ = "Copyright 2019, Tuan Nguyen"
__credits__ = ["Tuan Nguyen"]
__license__ = "GPL"
__version__ = "3.0"
__status__ = "Production"
__author__ = "TuanNguyen"
__email__ = "etuannv@gmail.com"
__website__ = "https://etuannv.com"

import socket
hostname = socket.gethostname()
if 'MD104' in hostname:
    ISLOCAL=True
else:
    ISLOCAL=False




import logging
import random
import os
import time
import sys
import re
import glob
import string
import csv
from hashlib import md5



#=======================================BEGIN LOGGING CONFIG ================================================
def configLogging(current_path):   
    #
    ## CONFIG LOG
    #
    globalLogLevel = logging.INFO
    #globalLogLevel = logging.DEBUG
    globalLogFormat = '%(asctime)s %(levelname)-4s %(filename)s:%(lineno)d %(message)s'
    globalLogFile = os.path.join(current_path, 'app.log')
    globalDateFmt = '%Y%m%d %H:%M:%S'

    # Config loggin global
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=globalLogLevel,
                        format=globalLogFormat,
                        datefmt=globalDateFmt,
                        filename=globalLogFile)

    # Config log to console
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(globalLogLevel)
    # set a format which is simpler for console use
    formatter = logging.Formatter(globalLogFormat, datefmt=globalDateFmt)
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

#=======================================END LOGGING CONFIG ================================================




#======================================= BEGIN UTILITY ================================================
def makeMD5(data):
    """make md5 string from input
    
    Arguments:
        data {any} -- input data
    
    Returns:
        string -- md5 string
    """    
    data = str(data)
    md_string = md5((data).encode('utf-8')).hexdigest()
    return md_string

def makeIdentify(data, ilen=100):
    """Make an identify from input
    
    Arguments:
        data {any type} -- Input data
    
    Keyword Arguments:
        ilen {int} -- Number of len that include in return result (default: {100})
    
    Returns:
        string -- identify string
    """    
    
    return '{}_{}'.format(data[:ilen] if len(data)>68 else data, makeMD5(data))

def regexMatchFirstResult(partern, stringdata, flags=0):
    """Get first result from match item and return dict
    Sample use: court = regexFirstResult(r'''\d  .*(?P<casenumber>\d{5,7}) (?P<name>.[^ ]+) (?P<complainant>.[^ ]+).*:(?P<attorney>.[^ ]+)''', line)
    
    Arguments:
        partern {string} -- regex expression
        stringdata {string} -- input string
    
    Keyword Arguments:
        flags {re.flags} -- flag for regex (default: {0})
    
    Returns:
        dict -- a dictionary of result
    """    
    m = re.match(partern, stringdata, flags)
    if m is not None:
        return m.groupdict()
    else:
        return None

def getFileExtension(file_name):
    ext = file_name.rsplit('.', 1)[1]
    return ext

def isValidUrl(url):
    regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not regex.match(url):
        return False
    else:
        return True
    

def extractEmails(url):
    response = rq.get(url)
    # print(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s))
    emails = re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b', response.text)
    if emails:
        for email in emails:
            if email not in emails:
                emails.append(email)
    return emails


def getCurrentDateString(format= '%Y-%m-%d %H:%M:%S'):
    ''' Get current date time string with format'''
    return time.strftime(format)

def confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """
    
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print ('Please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False



def getListFileWithExtension(file_path, ext = None):
    files = [f for f in glob.glob(file_path + "/" + str(ext))]
    return files

def getListFileInPath(dataPath, endwith = None):
    ''' Get list file in folder recusive '''
    result = []
    try:
        for root,files in os.walk(dataPath):
            for file in files:
                if endwith:
                    if file.endswith(endwith):
                        filename = os.path.join(root, file)
                        result.append(filename)
                else:
                    filename = os.path.join(root, file)
                    result.append(filename)
        return result
    except Exception as e:
        logging.error("Some thing wrong %s", e)
        return result


def removeHtmlTag(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def createFolderIfNotExists(folder_path):
    ''' Create a new folder if not exists'''
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def removeMoneySymbol(value):
    trim = re.compile(r'[^\d.,]+')
    value = trim.sub('', value)
    value = value.replace(",","")
    return value

def getRandomString(n=20):
    ''' Return random string'''
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(n))

def getRandomID(size=6, chars=string.ascii_uppercase + string.digits):
    ''' Return random string with number'''
    return ''.join(random.choice(chars) for _ in range(size))

def getUrlExtension(url):
    ''' Get extension of url'''
    ext = url.rsplit('.', 1)[1]
    return ext

def isAvailableUrl(url):
    '''
        Checking is url working or not
    '''
    result = False
    try:
        web = urlopen(url, timeout = 3.0)
        if web:
            code = web.getcode()
            result = code == 200
        else:
            result = False
    except:
        result = False
    return result

def get_extension(file_name):
    ext = file_name.rsplit('.', 1)[1]
    return ext

def removeMoneySymbol(value):
    trim = re.compile(r'[^\d.,]+')
    value = trim.sub('', value)
    value = value.replace(",",".")
    return value

def getQuantity(value):
    if value:
        value = re.findall(r'(\d+)', value, re.MULTILINE)
        if value:
            value = value[0]
        else:
            value = 0
    
    return value

def getMoney(value):
    if value is not None:
        trim = re.compile(r'[^\d.,]+')
        value = trim.sub('', value)
        value = value.replace(",","")
        return convertToFloat(value)
    else:
        return value
        
def convertToFloat(value):
    if value is None:
        return value
    try:
        return float(value)
    except ValueError:
        return None

def getFloatFromString(value):
    if value:
        value = re.findall(r'''([+-]?[0-9]*[.,]?[0-9]+)''', value, re.MULTILINE)
        if value:
            value = value[0]
            value.replace(',', '.')
            value = convertToFloat(value)
        else:
            value = None
    return value

def isValidUrl(url):
    regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not regex.match(url):
        return False
    else:
        return True
    

def extractEmails(url):
    response = rq.get(url)
    # print(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s))
    emails = re.findall(r'\b[\w.-]+?@\w+?\.\w+?\b', response.text)
    if emails:
        for email in emails:
            if email not in emails:
                emails.append(email)
    return emails


def getCurrentDateString(format= '%Y-%m-%d %H:%M:%S'):
    ''' Get current date time string with format'''
    return time.strftime(format)

def confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """
    
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print ('Please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False


#======================================= END UTILITY ================================================




#======================== BEGIN FILE UTILITY MODULE =========================
def readTextFileToList(filePath):
    ''' Read text file line by line to list '''
    if not os.path.isfile(filePath):
        logging.debug('File %s not found', filePath)
        return []
    
    with open(filePath) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    return content
            

def writeListToTextFile(list, filePath, mode='a'):
    ''' Write list to csv line by line '''
    with open(filePath, mode) as myfile:
        for item in list:
            myfile.write(str(item) +  '\n')

def writeListToCsvFile(data, filename, mode='a', header = 'None'):
    ''' Write list to csv file '''
    with open(filename, mode,newline="") as f:
        writer = csv.writer(f, delimiter=',')
        if header:
            writer.writerow(header)
        writer.writerows(data)

def readXlsFileToDict(filePath):
    from xlrd import open_workbook
    CurrentPath = os.path.dirname(os.path.realpath(sys.argv[0]))
    if not os.path.isfile(filePath):
        filePath = os.path.join(CurrentPath, filePath)
    if not os.path.isfile(filePath):
        logging.info("readXlsFileToDict - File not found")
    book = open_workbook(filePath)
    sheet = book.sheet_by_index(0)
    # read header values into the list    
    keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]
    dict_list = []
    for row_index in range(1, sheet.nrows):
        d = {keys[col_index]: sheet.cell(row_index, col_index).value 
            for col_index in range(sheet.ncols)}
        dict_list.append(d)

    return dict_list

def readCsvToList(filePath):
    ''' Read csv file to list'''
    if not os.path.isfile(filePath):
        logging.debug('File %s not found', filePath)
        return []
    with open(filePath, 'rb') as f:
        reader = csv.reader(f)
        return list(reader)

def readCsvToListDict(filePath):
    try:
        ''' Read csv file to list of dictionary'''
        if not os.path.isfile(filePath):
            logging.debug('File %s not found', filePath)
            return []

        result = []
        with open(filePath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result.append(row)
        return result
    except Exception as ex:
        logging.info(ex)
        return None

def readCsvToListDictWithHeader(filePath):
    ''' Read csv file to list of dictionary'''
    if not os.path.isfile(filePath):
        logging.debug('File %s not found', filePath)
        return []

    result = []
    with open(filePath, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)
    
    with open(filePath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append(row)
    
    return result, header

def writeDictToCSV(dict_data, csvFilePath, mode='w', headers=None):
    ''' Write list of dictionary to csv file'''
    try:
        isExistFile = os.path.isfile(csvFilePath)
        if not headers:
            headers = []
            for key in dict_data[0]:
                headers.append(key)

        with open(csvFilePath, mode) as f:
            writer = csv.writer(f)
            if ('a' in mode) and isExistFile:
                pass
            else:
                writer.writerow(headers)
            
            for row in dict_data:
                targetrow = []
                for key in headers:
                    targetrow.append(row[key])
                writer.writerow(targetrow)

        return True
    except IOError as e:
        logging.error("I/O error) %s", e)
        return False
    return True 
#======================== END FILE UTILITY MODULE =========================

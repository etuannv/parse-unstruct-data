#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = ["Tuan Nguyen"]
__copyright__ = "Copyright 2019, Tuan Nguyen"
__credits__ = ["Tuan Nguyen"]
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Production"
__author__ = "TuanNguyen"
__email__ = "etuannv@gmail.com"
__website__ = "https://etuannv.com"


MULTI_THREAD = False

# from etuannv import *

from etuannv import *
import shutil
import threading

def checkContinue():
    """Check if run continue
    
    Returns:
        bool -- return continue
    """    
    result = False
    if os.path.exists(TempFolderPath):
        #ask for continue
        os.system('clear')
        print ("============== ATTENTION !!! The previous session has not finished ==============")
        print("\n")
        is_continue = confirm(prompt='DO YOU WANT CONTINUE THE PREVIOUS SESSION?', resp=True)
        if not is_continue:
            logging.info("You choice start new session")
            print("\n")
            print("\n")
            try:
                # Delete all file in temp folder
                shutil.rmtree(TempFolderPath)
            except OSError:
                sys.exit("Error occur when delete temp folder")
            result = False
        else:
            logging.info("You choice continue previous session")
            print("\n")
            print("\n")
            result = True
    createFolderIfNotExists(TempFolderPath)
    return result


def getInputItem(total):
    """ pop input item by threading
    
    Arguments:
        total {int} -- total number of input list
    
    Returns:
        [type] -- [description]
    """    
    global ThreadLock, Input_Data
    item_no = len(Input_Data)
    if item_no > 0:
        # Get lock to synchronize threads  
        with ThreadLock:
            logging.info("Process {}/{}".format(total-item_no+1, total))
            item = Input_Data.pop(0)
            return item
    else:
        return None


def processItem(filepath):
    results = []
    rtemplate = {
        'casenumber': '',
        'name': '',
        'complainant': '',
        'attorney': '',
        'mistiminor or felony': '',
        'bond': '',
        'crime': '',
        'fingerprint': ''
    }

    # Read all line of file to list
    lines = readTextFileToList(filepath)

    level1 = None
    level2 = None
    level3 = None
    
    for line in lines:
        line = line.strip()
        
        # this for debug
        # if '000526' in line:
        #     print(line)
        #     import pdb ; pdb.set_trace()
        # court info
        court = regexMatchFirstResult(r'''\d+ +.[^ ]* (?P<casenumber>\d+) +(?P<name>.[^ ]*) +(?P<complainant>.[^ ]*)''', line)
        if court:
            level1 = rtemplate.copy()
            level1.update(court)
            attoney = regexMatchFirstResult(r'''.*:(?P<attorney>.[^ ]*)''', line)
            if attoney:
                level1.update(attoney)
            continue

        

        # figer printed
        if 'TO BE FINGERPRINTED' in line:
            if not level2:
                if not level1:
                    logging.warning('Missing level 1')
                    import pdb ; pdb.set_trace()
                else:
                    level2 = level1.copy()
                
            level2['fingerprint'] = 'TRUE'
            
            continue

        # bond info
        bond = regexMatchFirstResult(r'''BOND:\ +(?P<bond>\$+\d*[\,,\.]?\d{1,3})''', line)
        if bond:
            if not level2:
                if not level1:
                    logging.warning('Missing level 1')
                    import pdb ; pdb.set_trace()
                else:
                    level2 = level1.copy()
                
            level2.update(bond)
            
            continue

        
        
        # mistiminor or felony and crime
        
        mistiminor = regexMatchFirstResult(r'''\((?P<misti>.)\)(?P<crime>.[^:\(\)]+)''', line)
        
        if mistiminor:
            if level2 is not None:
                level3 = level2.copy()
                level2 = None
            elif level1 is not None:
                level3 = level1.copy()
            else:
                logging.warning('Missing level 1')
                import pdb ; pdb.set_trace()
            
            if 'misti' in mistiminor:
                level3['mistiminor or felony'] = mistiminor['misti']
            
            if 'crime' in mistiminor:
                level3['crime'] = mistiminor['crime'].replace('PLEA','')
            
            # write result
            # import pdb ; pdb.set_trace()
            results.append(level3)
            level3 = None


    return results
    


def mainWork(result_header):
    global ThreadLock
    
    
    total = len(Input_Data)
    # changeProxyTotal =50 -- Change proxy each 50 requests   
    browser = WebBrowser(timeout = 10, isDisableImage = False, isDisableJavascript = False)
    
    while True:
        print("\n")
        print("\n")
        data =  getInputItem(total)

        # If not data than return thread
        if data is None:
            break
        
        # If identify data in done list than skip
        identify_data = makeIdentify(data, 200)
        if identify_data in Done_List:
            continue
        result = processItem(browser, data)

        with ThreadLock:
            writeDictToCSV([result], ResultFilePath, 'a', result_header)
            # Write done file
            writeListToTextFile([identify_data], DoneFilePath, 'a')
            # Waiting for 3s to search next item
            time.sleep(.5)            
            

    browser.exitDriver()




if __name__ == "__main__":
    global CurrentPath, TempFolderPath, InputFilePath, DoneFilePath, ThreadNo, ThreadLock, Input_Data, Done_List
    CurrentPath = os.path.dirname(os.path.realpath(sys.argv[0]))
    InputFilePath = os.path.join(CurrentPath, 'input')
    
    TempFolderPath = os.path.join(CurrentPath, 'temp_result')
    DoneFilePath = os.path.join(TempFolderPath, 'done_item.txt')
    ResultFilePath = os.path.join(TempFolderPath, 'result.csv')
    ThreadNo = 1
    ThreadLock = threading.Lock()
    configLogging(CurrentPath)
    


    # ======= CHECK IF WANT TO CONTINUE PREVIOUS SESSION ========
    checkContinue()
   
    # ======= READ PREVIOUS SESSION ========
    # Get done category url list
    Done_List = readTextFileToList(DoneFilePath)
    
    # ======= START MAIN PROGRAM ========
    # READ INPUT FILE
    Input_Data = getListFileWithExtension(InputFilePath, '*.txt')
    if not len(Input_Data) > 0:
        logging.info('Not found input files in folder: {}'.format(InputFilePath))
        sys.exit("Not found input files in folder")


    result_header = [
        'casenumber',
        'name',
        'complainant',
        'attorney',
        'mistiminor or felony',
        'bond',
        'crime',
        'fingerprint'
    ]
    
    # Process input
    if MULTI_THREAD:   # Get multi thread
        ThreadLock = threading.Lock()
        thread_list = []
        logging.info('Run program with {} threads'.format(ThreadNo))
        for i in range(0, ThreadNo):
            # Start thread 1
            th = threading.Thread(target=mainWork, args=(result_header,))
            thread_list.append(th)
            th.start()
        
        for th in thread_list:
            th.join()
            time.sleep(.5)
    
    else:   # Get single thread
        counter = 0
        total = len(Input_Data)
        for data in Input_Data:
            identify_data = makeIdentify(data, 200)
            counter +=1
            logging.info("Process {}/{}".format(counter, total))
            result = processItem(data)

            if result is not None:
                writeDictToCSV(result, ResultFilePath, 'a', result_header)
        
            # Write done file
            writeListToTextFile([identify_data], DoneFilePath, 'a')

            # Waiting for 3s to search next item
            time.sleep(.5)
        



    # Done: Rename temp_folder to result folder
    if os.path.exists(TempFolderPath):
        result_folder_path = os.path.join(CurrentPath, 'result_{}'.format(getCurrentDateString(format='%Y%m%d_%Hh%M_%S')))
        os.rename(TempFolderPath, result_folder_path)

    logging.info("DONE !!! etuannv@gmail.com ;)")
    sys.exit()
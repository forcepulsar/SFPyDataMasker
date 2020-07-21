import requests
import json
import time
import sys
import os
from simple_salesforce import SalesforceLogin
from filesplit import FileSplit


csvfiles = []
jobs = []


def main():

    sObject = 'Account'
    fileName = 'newaccount.csv'
    splitCSVFiles(fileName)

    print(f'File(s) that will be processed: {csvfiles}')

    udpateDataInSF(sObject, csvfiles)

    # insertDataInSF(sObject, csvfiles)


def splitCSVFiles(fileName):
    maxBytesPerBatch = 100000000
    # maxBytesPerBatch = 2000

    if os.stat(fileName).st_size > maxBytesPerBatch:
        print(f'File: {fileName} will be split in smaller files...')
        fs = FileSplit(fileName, splitsize=maxBytesPerBatch)
        fs.split(include_header=True, callback=splitPrint)
    else:
        csvfiles.append(fileName)


def splitPrint(f, s, c):
    csvfiles.append(f)
    print(
        "File Name: {0}, size in bytes: {1}, number of lines: {2}".format(f, s, c))


def udpateDataInSF(sObject, csvfiles):
    session_id, instance = getSFconnection()
    for fileName in csvfiles:
        success, jobId = createUpdateJob(session_id, instance, sObject)
        if success:
            jobs.append(jobId)
            print(f'Job id created: {jobId}')
            isUploadSuccess = uploadCSVBatch(
                session_id, instance, jobId, fileName)
            closeJob(session_id, instance, jobId, isUploadSuccess)
            # TODO capture all the jobupload status and have a different process that follows results and gets errors
            # if isUploadSuccess:
            #     isJobSuccess = awaitJobCompletion(session_id, instance, jobId)
            #     getResults(session_id, instance, jobId, isJobSuccess)


def insertDataInSF(sObject, csvfiles):
    session_id, instance = getSFconnection()
    for fileName in csvfiles:
        success, jobId = createInsertJob(session_id, instance, sObject)
        if success:
            jobs.append(jobId)
            print(f'Job id created: {jobId}')
            isUploadSuccess = uploadCSVBatch(
                session_id, instance, jobId, fileName)
            closeJob(session_id, instance, jobId, isUploadSuccess)
            # TODO capture all the jobupload status and have a different process that follows results and gets errors
            # if isUploadSuccess:
            #     isJobSuccess = awaitJobCompletion(session_id, instance, jobId)
            #     getResults(session_id, instance, jobId, isJobSuccess)


def createUpdateJob(session_id, instance, sObject):
    headers = {
        'Authorization': 'Bearer ' + session_id,
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json',
    }

    job_def = '''{
        "operation" : "update",
        "object" : "%s",
        "lineEnding" : "LF",
        "contentType" : "CSV"
    }
    ''' % (sObject)

    url = 'https://%s/services/data/v48.0/jobs/ingest' % (instance)
    resp = requests.post(url, job_def, headers=headers)

    print('\nStatus of job creation: ' + str(resp.status_code))
    if str(resp.status_code) == '200':
        return (True, resp.json()['id'])
    else:
        print(json.dumps(resp.json(), indent=4))
        return (False, -1)


def createInsertJob(session_id, instance, sObject):
    headers = {
        'Authorization': 'Bearer ' + session_id,
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json',
    }

    job_def = '''{
        "operation" : "insert",
        "object" : "%s",
        "lineEnding" : "LF",
        "contentType" : "CSV"
    }
    ''' % (sObject)

    url = 'https://%s/services/data/v48.0/jobs/ingest' % (instance)
    resp = requests.post(url, job_def, headers=headers)

    print('\nStatus of job creation: ' + str(resp.status_code))
    if str(resp.status_code) == '200':
        return (True, resp.json()['id'])
    else:
        print(json.dumps(resp.json(), indent=4))
        return (False, -1)


def uploadCSVBatch(session_id, instance, jobId, fileName):
    print(f'Uploading csv file: {fileName}')
    headers = {
        'Authorization': 'Bearer ' + session_id,
        'Content-Type': 'text/csv',
        'Accept': 'application/json'
    }
    url = 'https://%s/services/data/v48.0/jobs/ingest/%s/batches' % (
        instance, jobId)

    f = open(fileName, "r")
    content = f.read()
    f.close()
    resp = requests.put(url, data=content, headers=headers)

    print(f'Status code for uploadCSVBatch: {resp.status_code}')
    if str(resp.status_code) == '201':
        return (True)
    else:
        print(f'Raw response uploadCSVBatch: {resp.text}')
        return (False)


def closeJob(session_id, instance, jobId, isUploadSuccess):
    headers = {
        'Authorization': 'Bearer ' + session_id,
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json'
    }
    url = 'https://%s/services/data/v48.0/jobs/ingest/%s' % (
        instance, jobId)
    body = ''
    message = ''
    if isUploadSuccess == True:
        job_def = '''{
            "state": "UploadComplete"
        }
        '''
        message = 'Closing job to start data processing'
    else:
        job_def = '''{
            "state": "Aborted"
        }
        '''
        message = 'Aborting the bulk api job as upload was not successful'

    print(message)
    resp = requests.patch(url, job_def, headers=headers)

    # print(json.dumps(resp.json(), indent=4))
    print(f'Status code for closeJob: {resp.status_code}')

    if str(resp.status_code) == '200':
        return True
    else:
        print(f'Raw response closeJob: {resp.text}')
        return False


def getResults(session_id, instance, jobId, isJobSuccess):
    headers = {
        'Authorization': 'Bearer ' + session_id,
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'text/csv',
    }

    if isJobSuccess == True:
        url = 'https://%s/services/data/v48.0/jobs/ingest/%s/successfulResults/' % (
            instance, jobId)
        # TODO capture the success results
    else:
        url = 'https://%s/services/data/v48.0/jobs/ingest/%s/failedResults/' % (
            instance, jobId)
        resp = requests.get(url, headers=headers)
        filename = 'errors'+jobId+'.csv'
        f = open(filename, 'w', errors="ignore")
        f.write(resp.text)

        f.close()
        print('Errors file created: ' + filename)

    # if str(resp.status_code) == '200':
    #     return True
    # else:
    #     return False


def awaitJobCompletion(session_id, instance, jobId):
    headers = {
        'Authorization': 'Bearer ' + session_id,
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json'
    }

    url = 'https://%s/services/data/v48.0/jobs/ingest/%s/' % (
        instance, jobId)

    while True:
        resp = requests.get(url, headers=headers)
        print(f'Raw response awaitJobCompletion: {resp.text}')
        print('\nStatus: of job completion: ' + str(resp.status_code))

        if resp.json()['state'] == 'JobComplete':
            return True
        elif resp.json()['state'] == 'Failed':
            return False
        else:
            print('Waiting few seconds for job to complete...')
            time.sleep(10)


def getSFconnection():
    # TODO create condition to validate when executed on a PRODUCTION environment
    # user would need to input manually the username to avoid prod data corruption
    return SalesforceLogin(
        username='<USERNAME>',
        password='<SFPASSWORD>',
        security_token='<SECURITYTOKEN>',
        domain='test')


def func(f, s, c):
    print("file: {0}, size: {1}, count: {2}".format(f, s, c))


if __name__ == "__main__":
    main()

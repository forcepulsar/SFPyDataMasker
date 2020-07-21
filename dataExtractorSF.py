import requests
import json
import time
from simple_salesforce import SalesforceLogin
from dataExtractorQueries import *


def main():
    isTestMode = False
    query = queryCaseUATRefresh
    fileName = 'case.csv'

    if isTestMode:
        query += ' LIMIT 2000'

    extractDataFromQuery(query, fileName)


def createQueryJob(instance, session_id, query):
    headers = {
        'Authorization': 'Bearer ' + session_id,
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json',
    }

    job_def = '''{
        "operation" : "queryAll",
        "query" : "%s"
    }
    ''' % (query)

    url = 'https://%s/services/data/v48.0/jobs/query' % (instance)
    resp = requests.post(url, job_def, headers=headers)

    print('Status of job creation: ' + str(resp.status_code))
    print(json.dumps(resp.json(), indent=4))
    if str(resp.status_code) == '200':
        return (True, resp.json()['id'])
    else:
        return (False, -1)


def awaitQueryJobCompletion(instance, session_id, jobId):
    headers = {'Authorization': 'Bearer ' + session_id}

    url = 'https://%s/services/data/v48.0/jobs/query/%s' % (
        instance, jobId)

    while True:
        resp = requests.get(url, headers=headers)
        print('\nStatus: of job completion ' + str(resp.status_code))
        # print(json.dumps(resp.json(), indent=4))
        print('Job Status: ' + resp.json()['state'])
        if resp.json()['state'] == 'JobComplete':
            break
        else:
            print('Waiting few seconds for job to complete...')
            time.sleep(10)


def downloadQueryResults(instance, session_id, jobId, fileName, maxRecords):
    headers = {'Authorization': 'Bearer ' + session_id}

    locator = 0
    f = open(fileName, 'w', errors="ignore")

    while True:
        url = 'https://%s/services/data/v48.0/jobs/query/%s/results?locator=%s&maxRecords=%s' % (
            instance, jobId, locator, maxRecords)

        resp = requests.get(url, headers=headers)

        print('\nStatus of data download: ' + str(resp.status_code))
        # print(resp.text)
        print('sforce locator: ' + str(resp.headers['Sforce-Locator']))
        if locator == 0:
            f.write(resp.text)
        else:
            f.write(resp.text.split("\n", 1)[1])
        locator = str(resp.headers['Sforce-Locator'])
        if locator == 'null':
            break

    f.close()
    print('file created: ' + fileName)


def extractDataFromQuery(query, fileName):

    session_id, instance = SalesforceLogin(
        username='<USERNAME>',
        password='<SFPASSWORD>',
        security_token='<SECURITYTOKEN>',
        domain='test')

    queryResult = createQueryJob(
        instance, session_id, query)

    jobId = queryResult[1] if queryResult[0] == True else -1
    print(jobId)
    print(queryResult)

    awaitQueryJobCompletion(instance, session_id, jobId)

    downloadQueryResults(instance, session_id, jobId,
                         fileName=fileName, maxRecords=100000)


if __name__ == "__main__":
    main()

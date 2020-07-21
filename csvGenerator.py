import random
import csv
import string
from csvTemplates import *
from datetime import datetime


def main():
    isTestMode = True

    fileName = 'case.csv'

    template = caseTemplate

    createCSV(fileName, template, isTestMode)


def createCSV(fileName, template, isTestMode):
    newFileName = 'NEW'+fileName
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    print('Start processing file: %s \nStart time: %s' %
          (fileName, timestampStr))

    with open(newFileName, 'w', newline='', encoding='utf-8') as f:
        fieldNames = template.keys()
        thewriter = csv.DictWriter(
            f, fieldnames=fieldNames, quoting=csv.QUOTE_ALL)
        thewriter.writeheader()

        with open(fileName) as file:
            reader = csv.DictReader(file)
            count = 0

            for row in reader:
                newRow = {}

                for key in template:
                    # checks for '-ifexists' in the template. If so, it checks there is a value
                    # on the original CSV.  If no value it will add #N/A to newCSV.
                    # If there is value, it will be processed by one of the field rules
                    if '-ifexists' in template[key] and len(row[key].strip()) == 0:
                        newRow[key] = '#N/A'
                    elif template[key] == 'id':
                        newRow[key] = row[key]
                    elif template[key] == 'blank':
                        newRow[key] = '#N/A'
                    elif 'firstname' in template[key]:
                        newRow[key] = randomWord()
                    elif 'fullname' in template[key]:
                        newRow[key] = randomWord()+' '+randomWord()
                    elif 'phone' in template[key]:
                        newRow[key] = randomPhoneNumber()
                    elif 'sentence' in template[key]:
                        newRow[key] = randomSentence()
                    elif 'emailAccount' in template[key]:
                        newRow[key] = emailWithAutoNumber(
                            row['AccountNumber__c'])
                    elif 'email' in template[key]:
                        newRow[key] = randomEmail()
                    elif 'street' in template[key]:
                        newRow[key] = '133 Castlereagh Street'
                    elif 'city' in template[key]:
                        newRow[key] = 'SYDNEY'
                    elif 'postcode' in template[key]:
                        newRow[key] = '2000'
                    elif 'state' in template[key]:
                        newRow[key] = 'NSW'
                    elif 'dob-ifexists-PersonBirthdate' in template[key]:
                        # TODO extract the original dob 'year' and add it to string, instead of making it all 1980
                        newRow[key] = '1980-01-01'
                    elif 'setphrase' in template[key]:
                        newRow[key] = 'Lorem ipsum dolor sit amet'

                # print(newRow)

                thewriter.writerow(newRow)
                count += 1
                if count == 20000 and isTestMode:
                    break

    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    print('Finished processing file: %s \nNumber of rows processed: %s \nFinished time: %s \nWith template:\n %s \nNew CSV file created: %s' % (
        fileName, count, timestampStr, template, newFileName))


def randomWord(stringLength=4):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, stringLength))


def randomSentence(numWords=3):
    sentence = ''
    for i in range(0, numWords):
        sentence += randomWord(3) + ' '
    return sentence.strip()


def randomNumber(stringLength=8):
    """Generate a random string of numbers of fixed length """
    numbers = string.digits
    return ''.join(random.sample(numbers, stringLength))


def randomPhoneNumber():
    return randomNumber(10)


def randomEmail():
    return f"test.{randomNumber()}{'@mydummydomain.com'}"


def emailWithAutoNumber(autonumber):
    return f"test.{autonumber}{'@mydummydomain.com'}"


if __name__ == "__main__":
    main()

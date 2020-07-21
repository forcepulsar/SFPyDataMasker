# The templates are used to create a new csv file
# New CSV will contain all the columns specified in the JSON template object
sampleTemplate = {
    'Id': 'id',  # Creates ID column. Id field ALWAYS must be in original file to be copied to new csv
    # Creates column with header Sample_Word__c, fills it with a random word
    'Sample_Word__c': 'firstname',
    # Creates column with header Sample_Blank__c, fills it with #N/A
    'Sample_Blank__c': 'blank',
    # Creates column with header Sample_Email__c, fills it with random email address
    'Sample_Email__c': 'email'
}

capaignTemplate = {
    'Id': 'id',
    'Main_Contact_First_Name__c': 'firstname-ifexists',
    'Main_Contact_Email__c': 'email-ifexists',
    'Notes__c': 'sentence'
}

caseTemplate = {
    'Id': 'id',
    'SuppliedName': 'fullname-ifexists',
    'SuppliedEmail': 'email-ifexists',
    'SuppliedPhone': 'phone-ifexists',
    'Subject': 'sentence',
    'Description': 'sentence'
}

accountTemplate = {
    'Id': 'id',
    'LastName': 'firstname',
    'PersonEmail': 'emailAccount',
    'AdditionalEmail__pc': 'email',
    'PersonHomePhone': 'phone',
    'PersonMobilePhone': 'phone',
    'PersonOtherPhone': 'phone',
    'Phone': 'phone',
    'PersonMailingPostalCode': 'postcode',
    'PersonMailingState': 'state',
    'PersonMailingCity': 'city',
    'PersonMailingStreet': 'street',
    'PersonOtherPostalCode': 'postcode',
    'PersonOtherState': 'state',
    'PersonOtherCity': 'city',
    'PersonOtherStreet': 'street',
    'PersonBirthdate': 'dob-ifexists-PersonBirthdate'
}

taskTemplate = {
    'Id': 'id',
    'Subject': 'sentence',
    'Description': 'sentence'
}

leadTemplate = {
    'Id': 'id',
    'Email': 'email',
    'LastName': 'firstname',
    'MobilePhone': 'phone',
    'PostalCode': 'postcode',
    'State': 'state',
    'City': 'city',
    'Street': 'street'
}

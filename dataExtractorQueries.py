queryLeadsConvertedUATRefresh = 'SELECT Id FROM Lead WHERE isConverted = true'

queryLeadsNONConvertedUATRefresh = 'SELECT Id FROM Lead WHERE isConverted = false'

queryAccountsUATRefresh = 'SELECT Id, AccountNumber__c, PersonBirthdate FROM Account WHERE IsPersonAccount = true'

queryCaseUATRefresh = 'Select Id, SuppliedName,SuppliedEmail, SuppliedPhone from Case'

queryCampaignsUATRefresh = 'Select Id, Main_Contact_First_Name__c, Main_Contact_Email__c from Campaign where (Main_Contact_First_Name__c <> null or Main_Contact_Email__c <> null )'

queryTasksUATRefresh = 'SELECT Id FROM Task '

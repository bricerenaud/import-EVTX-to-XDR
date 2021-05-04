# **** IMPORT A WINDOWS EVT FILE TO XDR DATASET ****
# (brenaud@paloaltonetworks.com)

# Script Dependencies to be installed
# pip3 install evtx flatten_json

# EVTX file must be copied directly from Windows station C:\Windows\System32\winevt\Logs

# --- CUSTOM COLLECTOR CONFIGURATION - TO BE COMPLETED BEFORE USE ---
#
# CUSTOM COLLECTOR's API KEY to be generated from XDR Console in Settings / Log Collections / Custom Collectors)
# Use uncompressed / JSON as Log Format  
# Do NOT use your generic Cortex API key, this is a different one!
#
# HTTP Custom Collector token key
api_key = ""
# HTTP Custom Collector url, click on "Copy api url" to get it and it should be something like:
# api_url = "https://api-yourinstance.xdr.eu.paloaltonetworks.com/logs/v1/event"
api_url = ""

# Number of events you'd like to import per API call
# If you receive of 413 error message in the import process decrease this number
# Generally, 2000 is a good number
api_block_size = 2000
#
# -------------------------------------------------------------------

# If DEBUG is set to 1, all the API call details (including payload size) will be displayed to the console
DEBUG = 1
GIT = "https://github.com/zoinx/import-EVTX-to-XDR"
VERSION = "0.9"

# Microsoft Windows EventID mapping table
# eventid category coming from: https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/
eventid = {
    "1100": {
        "category": "Non Audit",
        "name": "The event logging service has shut down"
    },
    "1101": {
        "category": "Non Audit",
        "name": "Audit events have been dropped by the transport."
    },
    "1102": {
        "category": "Non Audit",
        "name": "The audit log was cleared"
    },
    "1104": {
        "category": "Non Audit",
        "name": "The security Log is now full"
    },
    "1105": {
        "category": "Non Audit",
        "name": "Event log automatic backup"
    },
    "1108": {
        "category": "Non Audit",
        "name": "The event logging service encountered an error"
    },
    "4608": {
        "category": "System",
        "name": "Windows is starting up"
    },
    "4609": {
        "category": "System",
        "name": "Windows is shutting down"
    },
    "4610": {
        "category": "System",
        "name": "An authentication package has been loaded by the Local Security Authority"
    },
    "4611": {
        "category": "System",
        "name": "A trusted logon process has been registered with the Local Security Authority"
    },
    "4612": {
        "category": "System",
        "name": "Internal resources allocated for the queuing of audit messages have been exhausted, leading to the loss of some audits."
    },
    "4614": {
        "category": "System",
        "name": "A notification package has been loaded by the Security Account Manager."
    },
    "4615": {
        "category": "System",
        "name": "Invalid use of LPC port"
    },
    "4616": {
        "category": "System",
        "name": "The system time was changed."
    },
    "4618": {
        "category": "System",
        "name": "A monitored security event pattern has occurred"
    },
    "4621": {
        "category": "System",
        "name": "Administrator recovered system from CrashOnAuditFail"
    },
    "4622": {
        "category": "System",
        "name": "A security package has been loaded by the Local Security Authority."
    },
    "4624": {
        "category": "Logon Logoff",
        "name": "An account was successfully logged on"
    },
    "4625": {
        "category": "Logon Logoff",
        "name": "An account failed to log on"
    },
    "4626": {
        "category": "Logon Logoff",
        "name": "User/Device claims information"
    },
    "4627": {
        "category": "Logon Logoff",
        "name": "Group membership information."
    },
    "4634": {
        "category": "Logon Logoff",
        "name": "An account was logged off"
    },
    "4646": {
        "category": "Logon Logoff",
        "name": "IKE DoS-prevention mode started"
    },
    "4647": {
        "category": "Logon Logoff",
        "name": "User initiated logoff"
    },
    "4648": {
        "category": "Logon Logoff",
        "name": "A logon was attempted using explicit credentials"
    },
    "4649": {
        "category": "Logon Logoff",
        "name": "A replay attack was detected"
    },
    "4650": {
        "category": "Logon Logoff",
        "name": "An IPsec Main Mode security association was established"
    },
    "4651": {
        "category": "Logon Logoff",
        "name": "An IPsec Main Mode security association was established"
    },
    "4652": {
        "category": "Logon Logoff",
        "name": "An IPsec Main Mode negotiation failed"
    },
    "4653": {
        "category": "Logon Logoff",
        "name": "An IPsec Main Mode negotiation failed"
    },
    "4654": {
        "category": "Logon Logoff",
        "name": "An IPsec Quick Mode negotiation failed"
    },
    "4655": {
        "category": "Logon Logoff",
        "name": "An IPsec Main Mode security association ended"
    },
    "4656": {
        "category": "Object Access",
        "name": "A handle to an object was requested"
    },
    "4657": {
        "category": "Object Access",
        "name": "A registry value was modified"
    },
    "4658": {
        "category": "Object Access",
        "name": "The handle to an object was closed"
    },
    "4659": {
        "category": "Object Access",
        "name": "A handle to an object was requested with intent to delete"
    },
    "4660": {
        "category": "Object Access",
        "name": "An object was deleted"
    },
    "4661": {
        "category": "Object Access",
        "name": "A handle to an object was requested"
    },
    "4662": {
        "category": "Directory Services",
        "name": "An operation was performed on an object"
    },
    "4663": {
        "category": "Object Access",
        "name": "An attempt was made to access an object"
    },
    "4664": {
        "category": "Object Access",
        "name": "An attempt was made to create a hard link"
    },
    "4665": {
        "category": "Object Access",
        "name": "An attempt was made to create an application client context."
    },
    "4666": {
        "category": "Object Access",
        "name": "An application attempted an operation"
    },
    "4667": {
        "category": "Object Access",
        "name": "An application client context was deleted"
    },
    "4668": {
        "category": "Object Access",
        "name": "An application was initialized"
    },
    "4670": {
        "category": "Policy Change",
        "name": "Permissions on an object were changed"
    },
    "4671": {
        "category": "Object Access",
        "name": "An application attempted to access a blocked ordinal through the TBS"
    },
    "4672": {
        "category": "Logon Logoff",
        "name": "Special privileges assigned to new logon"
    },
    "4673": {
        "category": "Privilege Use",
        "name": "A privileged service was called"
    },
    "4674": {
        "category": "Privilege Use",
        "name": "An operation was attempted on a privileged object"
    },
    "4675": {
        "category": "Logon Logoff",
        "name": "SIDs were filtered"
    },
    "4688": {
        "category": "Process Tracking",
        "name": "A new process has been created"
    },
    "4689": {
        "category": "Process Tracking",
        "name": "A process has exited"
    },
    "4690": {
        "category": "Object Access",
        "name": "An attempt was made to duplicate a handle to an object"
    },
    "4691": {
        "category": "Object Access",
        "name": "Indirect access to an object was requested"
    },
    "4692": {
        "category": "Process Tracking",
        "name": "Backup of data protection master key was attempted"
    },
    "4693": {
        "category": "Process Tracking",
        "name": "Recovery of data protection master key was attempted"
    },
    "4694": {
        "category": "Process Tracking",
        "name": "Protection of auditable protected data was attempted"
    },
    "4695": {
        "category": "Process Tracking",
        "name": "Unprotection of auditable protected data was attempted"
    },
    "4696": {
        "category": "Process Tracking",
        "name": "A primary token was assigned to process"
    },
    "4697": {
        "category": "System",
        "name": "A service was installed in the system"
    },
    "4698": {
        "category": "Object Access",
        "name": "A scheduled task was created"
    },
    "4699": {
        "category": "Object Access",
        "name": "A scheduled task was deleted"
    },
    "4700": {
        "category": "Object Access",
        "name": "A scheduled task was enabled"
    },
    "4701": {
        "category": "Object Access",
        "name": "A scheduled task was disabled"
    },
    "4702": {
        "category": "Object Access",
        "name": "A scheduled task was updated"
    },
    "4703": {
        "category": "Policy Change",
        "name": "A token right was adjusted"
    },
    "4704": {
        "category": "Policy Change",
        "name": "A user right was assigned"
    },
    "4705": {
        "category": "Policy Change",
        "name": "A user right was removed"
    },
    "4706": {
        "category": "Policy Change",
        "name": "A new trust was created to a domain"
    },
    "4707": {
        "category": "Policy Change",
        "name": "A trust to a domain was removed"
    },
    "4709": {
        "category": "Policy Change",
        "name": "IPsec Services was started"
    },
    "4710": {
        "category": "Policy Change",
        "name": "IPsec Services was disabled"
    },
    "4711": {
        "category": "Policy Change",
        "name": "PAStore Engine"
    },
    "4712": {
        "category": "Policy Change",
        "name": "IPsec Services encountered a potentially serious failure"
    },
    "4713": {
        "category": "Policy Change",
        "name": "Kerberos policy was changed"
    },
    "4714": {
        "category": "Policy Change",
        "name": "Encrypted data recovery policy was changed"
    },
    "4715": {
        "category": "Policy Change",
        "name": "The audit policy (SACL) on an object was changed"
    },
    "4716": {
        "category": "Policy Change",
        "name": "Trusted domain information was modified"
    },
    "4717": {
        "category": "Policy Change",
        "name": "System security access was granted to an account"
    },
    "4718": {
        "category": "Policy Change",
        "name": "System security access was removed from an account"
    },
    "4719": {
        "category": "Policy Change",
        "name": "System audit policy was changed"
    },
    "4720": {
        "category": "Account Management",
        "name": "A user account was created"
    },
    "4722": {
        "category": "Account Management",
        "name": "A user account was enabled"
    },
    "4723": {
        "category": "Account Management",
        "name": "An attempt was made to change an account's password"
    },
    "4724": {
        "category": "Account Management",
        "name": "An attempt was made to reset an accounts password"
    },
    "4725": {
        "category": "Account Management",
        "name": "A user account was disabled"
    },
    "4726": {
        "category": "Account Management",
        "name": "A user account was deleted"
    },
    "4727": {
        "category": "Account Management",
        "name": "A security-enabled global group was created"
    },
    "4728": {
        "category": "Account Management",
        "name": "A member was added to a security-enabled global group"
    },
    "4729": {
        "category": "Account Management",
        "name": "A member was removed from a security-enabled global group"
    },
    "4730": {
        "category": "Account Management",
        "name": "A security-enabled global group was deleted"
    },
    "4731": {
        "category": "Account Management",
        "name": "A security-enabled local group was created"
    },
    "4732": {
        "category": "Account Management",
        "name": "A member was added to a security-enabled local group"
    },
    "4733": {
        "category": "Account Management",
        "name": "A member was removed from a security-enabled local group"
    },
    "4734": {
        "category": "Account Management",
        "name": "A security-enabled local group was deleted"
    },
    "4735": {
        "category": "Account Management",
        "name": "A security-enabled local group was changed"
    },
    "4737": {
        "category": "Account Management",
        "name": "A security-enabled global group was changed"
    },
    "4738": {
        "category": "Account Management",
        "name": "A user account was changed"
    },
    "4739": {
        "category": "Account Management",
        "name": "Domain Policy was changed"
    },
    "4740": {
        "category": "Account Management",
        "name": "A user account was locked out"
    },
    "4741": {
        "category": "Account Management",
        "name": "A computer account was created"
    },
    "4742": {
        "category": "Account Management",
        "name": "A computer account was changed"
    },
    "4743": {
        "category": "Account Management",
        "name": "A computer account was deleted"
    },
    "4744": {
        "category": "Account Management",
        "name": "A security-disabled local group was created"
    },
    "4745": {
        "category": "Account Management",
        "name": "A security-disabled local group was changed"
    },
    "4746": {
        "category": "Account Management",
        "name": "A member was added to a security-disabled local group"
    },
    "4747": {
        "category": "Account Management",
        "name": "A member was removed from a security-disabled local group"
    },
    "4748": {
        "category": "Account Management",
        "name": "A security-disabled local group was deleted"
    },
    "4749": {
        "category": "Account Management",
        "name": "A security-disabled global group was created"
    },
    "4750": {
        "category": "Account Management",
        "name": "A security-disabled global group was changed"
    },
    "4751": {
        "category": "Account Management",
        "name": "A member was added to a security-disabled global group"
    },
    "4752": {
        "category": "Account Management",
        "name": "A member was removed from a security-disabled global group"
    },
    "4753": {
        "category": "Account Management",
        "name": "A security-disabled global group was deleted"
    },
    "4754": {
        "category": "Account Management",
        "name": "A security-enabled universal group was created"
    },
    "4755": {
        "category": "Account Management",
        "name": "A security-enabled universal group was changed"
    },
    "4756": {
        "category": "Account Management",
        "name": "A member was added to a security-enabled universal group"
    },
    "4757": {
        "category": "Account Management",
        "name": "A member was removed from a security-enabled universal group"
    },
    "4758": {
        "category": "Account Management",
        "name": "A security-enabled universal group was deleted"
    },
    "4759": {
        "category": "Account Management",
        "name": "A security-disabled universal group was created"
    },
    "4760": {
        "category": "Account Management",
        "name": "A security-disabled universal group was changed"
    },
    "4761": {
        "category": "Account Management",
        "name": "A member was added to a security-disabled universal group"
    },
    "4762": {
        "category": "Account Management",
        "name": "A member was removed from a security-disabled universal group"
    },
    "4763": {
        "category": "Account Management",
        "name": "A security-disabled universal group was deleted"
    },
    "4764": {
        "category": "Account Management",
        "name": "A groups type was changed"
    },
    "4765": {
        "category": "Account Management",
        "name": "SID History was added to an account"
    },
    "4766": {
        "category": "Account Management",
        "name": "An attempt to add SID History to an account failed"
    },
    "4767": {
        "category": "Account Management",
        "name": "A user account was unlocked"
    },
    "4768": {
        "category": "Account Logon",
        "name": "A Kerberos authentication ticket (TGT) was requested"
    },
    "4769": {
        "category": "Account Logon",
        "name": "A Kerberos service ticket was requested"
    },
    "4770": {
        "category": "Account Logon",
        "name": "A Kerberos service ticket was renewed"
    },
    "4771": {
        "category": "Account Logon",
        "name": "Kerberos pre-authentication failed"
    },
    "4772": {
        "category": "Account Logon",
        "name": "A Kerberos authentication ticket request failed"
    },
    "4773": {
        "category": "Account Logon",
        "name": "A Kerberos service ticket request failed"
    },
    "4774": {
        "category": "Account Logon",
        "name": "An account was mapped for logon"
    },
    "4775": {
        "category": "Account Logon",
        "name": "An account could not be mapped for logon"
    },
    "4776": {
        "category": "Account Logon",
        "name": "The domain controller attempted to validate the credentials for an account"
    },
    "4777": {
        "category": "Account Logon",
        "name": "The domain controller failed to validate the credentials for an account"
    },
    "4778": {
        "category": "Logon Logoff",
        "name": "A session was reconnected to a Window Station"
    },
    "4779": {
        "category": "Logon Logoff",
        "name": "A session was disconnected from a Window Station"
    },
    "4780": {
        "category": "Account Management",
        "name": "The ACL was set on accounts which are members of administrators groups"
    },
    "4781": {
        "category": "Account Management",
        "name": "The name of an account was changed"
    },
    "4782": {
        "category": "Account Management",
        "name": "The password hash an account was accessed"
    },
    "4783": {
        "category": "Account Management",
        "name": "A basic application group was created"
    },
    "4784": {
        "category": "Account Management",
        "name": "A basic application group was changed"
    },
    "4785": {
        "category": "Account Management",
        "name": "A member was added to a basic application group"
    },
    "4786": {
        "category": "Account Management",
        "name": "A member was removed from a basic application group"
    },
    "4787": {
        "category": "Account Management",
        "name": "A non-member was added to a basic application group"
    },
    "4788": {
        "category": "Account Management",
        "name": "A non-member was removed from a basic application group.."
    },
    "4789": {
        "category": "Account Management",
        "name": "A basic application group was deleted"
    },
    "4790": {
        "category": "Account Management",
        "name": "An LDAP query group was created"
    },
    "4791": {
        "category": "Account Management",
        "name": "A basic application group was changed"
    },
    "4792": {
        "category": "Account Management",
        "name": "An LDAP query group was deleted"
    },
    "4793": {
        "category": "Account Management",
        "name": "The Password Policy Checking API was called"
    },
    "4794": {
        "category": "Account Management",
        "name": "An attempt was made to set the Directory Services Restore Mode administrator password"
    },
    "4797": {
        "category": "Account Management",
        "name": "An attempt was made to query the existence of a blank password for an account"
    },
    "4798": {
        "category": "Account Management",
        "name": "A user's local group membership was enumerated."
    },
    "4799": {
        "category": "Account Management",
        "name": "A security-enabled local group membership was enumerated"
    },
    "4800": {
        "category": "Logon Logoff",
        "name": "The workstation was locked"
    },
    "4801": {
        "category": "Logon Logoff",
        "name": "The workstation was unlocked"
    },
    "4802": {
        "category": "Logon Logoff",
        "name": "The screen saver was invoked"
    },
    "4803": {
        "category": "Logon Logoff",
        "name": "The screen saver was dismissed"
    },
    "4816": {
        "category": "Process Tracking",
        "name": "RPC detected an integrity violation while decrypting an incoming message"
    },
    "4817": {
        "category": "Policy Change",
        "name": "Auditing settings on object were changed."
    },
    "4818": {
        "category": "Object Access",
        "name": "Proposed Central Access Policy does not grant the same access permissions as the current Central Access Policy"
    },
    "4819": {
        "category": "Policy Change",
        "name": "Central Access Policies on the machine have been changed"
    },
    "4820": {
        "category": "Account Logon",
        "name": "A Kerberos Ticket-granting-ticket (TGT) was denied because the device does not meet the access control restrictions"
    },
    "4821": {
        "category": "System",
        "name": "A Kerberos service ticket was denied because the user, device, or both does not meet the access control restrictions"
    },
    "4822": {
        "category": "System",
        "name": "NTLM authentication failed because the account was a member of the Protected User group"
    },
    "4823": {
        "category": "System",
        "name": "NTLM authentication failed because access control restrictions are required"
    },
    "4824": {
        "category": "System",
        "name": "Kerberos preauthentication by using DES or RC4 failed because the account was a member of the Protected User group"
    },
    "4825": {
        "category": "System",
        "name": "A user was denied the access to Remote Desktop. By default, users are allowed to connect only if they are members of the Remote Desktop Users group or Administrators group"
    },
    "4826": {
        "category": "Policy Change",
        "name": "Boot Configuration Data loaded"
    },
    "4830": {
        "category": "System",
        "name": "SID History was removed from an account"
    },
    "4864": {
        "category": "Uncategorized",
        "name": "A namespace collision was detected"
    },
    "4865": {
        "category": "Policy Change",
        "name": "A trusted forest information entry was added"
    },
    "4866": {
        "category": "Policy Change",
        "name": "A trusted forest information entry was removed"
    },
    "4867": {
        "category": "Policy Change",
        "name": "A trusted forest information entry was modified"
    },
    "4868": {
        "category": "Object Access",
        "name": "The certificate manager denied a pending certificate request"
    },
    "4869": {
        "category": "Object Access",
        "name": "Certificate Services received a resubmitted certificate request"
    },
    "4870": {
        "category": "Object Access",
        "name": "Certificate Services revoked a certificate"
    },
    "4871": {
        "category": "Object Access",
        "name": "Certificate Services received a request to publish the certificate revocation list (CRL)"
    },
    "4872": {
        "category": "Object Access",
        "name": "Certificate Services published the certificate revocation list (CRL)"
    },
    "4873": {
        "category": "Object Access",
        "name": "A certificate request extension changed"
    },
    "4874": {
        "category": "Object Access",
        "name": "One or more certificate request attributes changed."
    },
    "4875": {
        "category": "Object Access",
        "name": "Certificate Services received a request to shut down"
    },
    "4876": {
        "category": "Object Access",
        "name": "Certificate Services backup started"
    },
    "4877": {
        "category": "Object Access",
        "name": "Certificate Services backup completed"
    },
    "4878": {
        "category": "Object Access",
        "name": "Certificate Services restore started"
    },
    "4879": {
        "category": "Object Access",
        "name": "Certificate Services restore completed"
    },
    "4880": {
        "category": "Object Access",
        "name": "Certificate Services started"
    },
    "4881": {
        "category": "Object Access",
        "name": "Certificate Services stopped"
    },
    "4882": {
        "category": "Object Access",
        "name": "The security permissions for Certificate Services changed"
    },
    "4883": {
        "category": "Object Access",
        "name": "Certificate Services retrieved an archived key"
    },
    "4884": {
        "category": "Object Access",
        "name": "Certificate Services imported a certificate into its database"
    },
    "4885": {
        "category": "Object Access",
        "name": "The audit filter for Certificate Services changed"
    },
    "4886": {
        "category": "Object Access",
        "name": "Certificate Services received a certificate request"
    },
    "4887": {
        "category": "Object Access",
        "name": "Certificate Services approved a certificate request and issued a certificate"
    },
    "4888": {
        "category": "Object Access",
        "name": "Certificate Services denied a certificate request"
    },
    "4889": {
        "category": "Object Access",
        "name": "Certificate Services set the status of a certificate request to pending"
    },
    "4890": {
        "category": "Object Access",
        "name": "The certificate manager settings for Certificate Services changed."
    },
    "4891": {
        "category": "Object Access",
        "name": "A configuration entry changed in Certificate Services"
    },
    "4892": {
        "category": "Object Access",
        "name": "A property of Certificate Services changed"
    },
    "4893": {
        "category": "Object Access",
        "name": "Certificate Services archived a key"
    },
    "4894": {
        "category": "Object Access",
        "name": "Certificate Services imported and archived a key"
    },
    "4895": {
        "category": "Object Access",
        "name": "Certificate Services published the CA certificate to Active Directory Domain Services"
    },
    "4896": {
        "category": "Object Access",
        "name": "One or more rows have been deleted from the certificate database"
    },
    "4897": {
        "category": "Object Access",
        "name": "Role separation enabled"
    },
    "4898": {
        "category": "Object Access",
        "name": "Certificate Services loaded a template"
    },
    "4899": {
        "category": "Object Access",
        "name": "A Certificate Services template was updated"
    },
    "4900": {
        "category": "Object Access",
        "name": "Certificate Services template security was updated"
    },
    "4902": {
        "category": "Policy Change",
        "name": "The Per-user audit policy table was created"
    },
    "4904": {
        "category": "Policy Change",
        "name": "An attempt was made to register a security event source"
    },
    "4905": {
        "category": "Policy Change",
        "name": "An attempt was made to unregister a security event source"
    },
    "4906": {
        "category": "Policy Change",
        "name": "The CrashOnAuditFail value has changed"
    },
    "4907": {
        "category": "Policy Change",
        "name": "Auditing settings on object were changed"
    },
    "4908": {
        "category": "Policy Change",
        "name": "Special Groups Logon table modified"
    },
    "4909": {
        "category": "Uncategorized",
        "name": "The local policy settings for the TBS were changed"
    },
    "4910": {
        "category": "Uncategorized",
        "name": "The group policy settings for the TBS were changed"
    },
    "4911": {
        "category": "Policy Change",
        "name": "Resource attributes of the object were changed"
    },
    "4912": {
        "category": "Policy Change",
        "name": "Per User Audit Policy was changed"
    },
    "4913": {
        "category": "Policy Change",
        "name": "Central Access Policy on the object was changed"
    },
    "4928": {
        "category": "Directory Services",
        "name": "An Active Directory replica source naming context was established"
    },
    "4929": {
        "category": "Directory Services",
        "name": "An Active Directory replica source naming context was removed"
    },
    "4930": {
        "category": "Directory Services",
        "name": "An Active Directory replica source naming context was modified"
    },
    "4931": {
        "category": "Directory Services",
        "name": "An Active Directory replica destination naming context was modified"
    },
    "4932": {
        "category": "Directory Services",
        "name": "Synchronization of a replica of an Active Directory naming context has begun"
    },
    "4933": {
        "category": "Directory Services",
        "name": "Synchronization of a replica of an Active Directory naming context has ended"
    },
    "4934": {
        "category": "Directory Services",
        "name": "Attributes of an Active Directory object were replicated"
    },
    "4935": {
        "category": "Directory Services",
        "name": "Replication failure begins"
    },
    "4936": {
        "category": "Directory Services",
        "name": "Replication failure ends"
    },
    "4937": {
        "category": "Directory Services",
        "name": "A lingering object was removed from a replica"
    },
    "4944": {
        "category": "Policy Change",
        "name": "The following policy was active when the Windows Firewall started"
    },
    "4945": {
        "category": "Policy Change",
        "name": "A rule was listed when the Windows Firewall started"
    },
    "4946": {
        "category": "Policy Change",
        "name": "A change has been made to Windows Firewall exception list. A rule was added"
    },
    "4947": {
        "category": "Policy Change",
        "name": "A change has been made to Windows Firewall exception list. A rule was modified"
    },
    "4948": {
        "category": "Policy Change",
        "name": "A change has been made to Windows Firewall exception list. A rule was deleted"
    },
    "4949": {
        "category": "Policy Change",
        "name": "Windows Firewall settings were restored to the default values"
    },
    "4950": {
        "category": "Policy Change",
        "name": "A Windows Firewall setting has changed"
    },
    "4951": {
        "category": "Policy Change",
        "name": "A rule has been ignored because its major version number was not recognized by Windows Firewall"
    },
    "4952": {
        "category": "Policy Change",
        "name": "Parts of a rule have been ignored because its minor version number was not recognized by Windows Firewall"
    },
    "4953": {
        "category": "Uncategorized",
        "name": "A rule has been ignored by Windows Firewall because it could not parse the rule"
    },
    "4954": {
        "category": "Policy Change",
        "name": "Windows Firewall Group Policy settings has changed. The new settings have been applied"
    },
    "4956": {
        "category": "Policy Change",
        "name": "Windows Firewall has changed the active profile"
    },
    "4957": {
        "category": "Policy Change",
        "name": "Windows Firewall did not apply the following rule"
    },
    "4958": {
        "category": "Policy Change",
        "name": "Windows Firewall did not apply the following rule because the rule referred to items not configured on this computer"
    },
    "4960": {
        "category": "Uncategorized",
        "name": "IPsec dropped an inbound packet that failed an integrity check"
    },
    "4961": {
        "category": "Uncategorized",
        "name": "IPsec dropped an inbound packet that failed a replay check"
    },
    "4962": {
        "category": "Uncategorized",
        "name": "IPsec dropped an inbound packet that failed a replay check"
    },
    "4963": {
        "category": "Uncategorized",
        "name": "IPsec dropped an inbound clear text packet that should have been secured"
    },
    "4964": {
        "category": "Logon Logoff",
        "name": "Special groups have been assigned to a new logon"
    },
    "4965": {
        "category": "Uncategorized",
        "name": "IPsec received a packet from a remote computer with an incorrect Security Parameter Index (SPI)."
    },
    "4976": {
        "category": "Logon Logoff",
        "name": "During Main Mode negotiation, IPsec received an invalid negotiation packet."
    },
    "4977": {
        "category": "Logon Logoff",
        "name": "During Quick Mode negotiation, IPsec received an invalid negotiation packet."
    },
    "4978": {
        "category": "Logon Logoff",
        "name": "During Extended Mode negotiation, IPsec received an invalid negotiation packet."
    },
    "4979": {
        "category": "Logon Logoff",
        "name": "IPsec Main Mode and Extended Mode security associations were established."
    },
    "4980": {
        "category": "Logon Logoff",
        "name": "IPsec Main Mode and Extended Mode security associations were established"
    },
    "4981": {
        "category": "Logon Logoff",
        "name": "IPsec Main Mode and Extended Mode security associations were established"
    },
    "4982": {
        "category": "Logon Logoff",
        "name": "IPsec Main Mode and Extended Mode security associations were established"
    },
    "4983": {
        "category": "Logon Logoff",
        "name": "An IPsec Extended Mode negotiation failed"
    },
    "4984": {
        "category": "Logon Logoff",
        "name": "An IPsec Extended Mode negotiation failed"
    },
    "4985": {
        "category": "Object Access",
        "name": "The state of a transaction has changed"
    },
    "5024": {
        "category": "System",
        "name": "The Windows Firewall Service has started successfully"
    },
    "5025": {
        "category": "System",
        "name": "The Windows Firewall Service has been stopped"
    },
    "5027": {
        "category": "System",
        "name": "The Windows Firewall Service was unable to retrieve the security policy from the local storage"
    },
    "5028": {
        "category": "System",
        "name": "The Windows Firewall Service was unable to parse the new security policy."
    },
    "5029": {
        "category": "System",
        "name": "The Windows Firewall Service failed to initialize the driver"
    },
    "5030": {
        "category": "System",
        "name": "The Windows Firewall Service failed to start"
    },
    "5031": {
        "category": "Object Access",
        "name": "The Windows Firewall Service blocked an application from accepting incoming connections on the network."
    },
    "5032": {
        "category": "System",
        "name": "Windows Firewall was unable to notify the user that it blocked an application from accepting incoming connections on the network"
    },
    "5033": {
        "category": "System",
        "name": "The Windows Firewall Driver has started successfully"
    },
    "5034": {
        "category": "System",
        "name": "The Windows Firewall Driver has been stopped"
    },
    "5035": {
        "category": "System",
        "name": "The Windows Firewall Driver failed to start"
    },
    "5037": {
        "category": "System",
        "name": "The Windows Firewall Driver detected critical runtime error. Terminating"
    },
    "5038": {
        "category": "System",
        "name": "Code integrity determined that the image hash of a file is not valid"
    },
    "5039": {
        "category": "Uncategorized",
        "name": "A registry key was virtualized."
    },
    "5040": {
        "category": "Uncategorized",
        "name": "A change has been made to IPsec settings. An Authentication Set was added."
    },
    "5041": {
        "category": "Uncategorized",
        "name": "A change has been made to IPsec settings. An Authentication Set was modified"
    },
    "5042": {
        "category": "Uncategorized",
        "name": "A change has been made to IPsec settings. An Authentication Set was deleted"
    },
    "5043": {
        "category": "Uncategorized",
        "name": "A change has been made to IPsec settings. A Connection Security Rule was added"
    },
    "5044": {
        "category": "Uncategorized",
        "name": "A change has been made to IPsec settings. A Connection Security Rule was modified"
    },
    "5045": {
        "category": "Uncategorized",
        "name": "A change has been made to IPsec settings. A Connection Security Rule was deleted"
    },
    "5046": {
        "category": "Uncategorized",
        "name": "A change has been made to IPsec settings. A Crypto Set was added"
    },
    "5047": {
        "category": "Uncategorized",
        "name": "A change has been made to IPsec settings. A Crypto Set was modified"
    },
    "5048": {
        "category": "Uncategorized",
        "name": "A change has been made to IPsec settings. A Crypto Set was deleted"
    },
    "5049": {
        "category": "Uncategorized",
        "name": "An IPsec Security Association was deleted"
    },
    "5050": {
        "category": "Uncategorized",
        "name": "An attempt to programmatically disable the Windows Firewall using a call to INetFwProfile.FirewallEnabled(FALSE"
    },
    "5051": {
        "category": "Uncategorized",
        "name": "A file was virtualized"
    },
    "5056": {
        "category": "System",
        "name": "A cryptographic self test was performed"
    },
    "5057": {
        "category": "Uncategorized",
        "name": "A cryptographic primitive operation failed"
    },
    "5058": {
        "category": "System",
        "name": "Key file operation"
    },
    "5059": {
        "category": "System",
        "name": "Key migration operation"
    },
    "5060": {
        "category": "Uncategorized",
        "name": "Verification operation failed"
    },
    "5061": {
        "category": "System",
        "name": "Cryptographic operation"
    },
    "5062": {
        "category": "Uncategorized",
        "name": "A kernel-mode cryptographic self test was performed"
    },
    "5063": {
        "category": "Policy Change",
        "name": "A cryptographic provider operation was attempted"
    },
    "5064": {
        "category": "Policy Change",
        "name": "A cryptographic context operation was attempted"
    },
    "5065": {
        "category": "Policy Change",
        "name": "A cryptographic context modification was attempted"
    },
    "5066": {
        "category": "Policy Change",
        "name": "A cryptographic function operation was attempted"
    },
    "5067": {
        "category": "Policy Change",
        "name": "A cryptographic function modification was attempted"
    },
    "5068": {
        "category": "Policy Change",
        "name": "A cryptographic function provider operation was attempted"
    },
    "5069": {
        "category": "Policy Change",
        "name": "A cryptographic function property operation was attempted"
    },
    "5070": {
        "category": "Policy Change",
        "name": "A cryptographic function property operation was attempted"
    },
    "5071": {
        "category": "System",
        "name": "Key access denied by Microsoft key distribution service"
    },
    "5120": {
        "category": "Object Access",
        "name": "OCSP Responder Service Started"
    },
    "5121": {
        "category": "Uncategorized",
        "name": "OCSP Responder Service Stopped"
    },
    "5122": {
        "category": "Uncategorized",
        "name": "A Configuration entry changed in the OCSP Responder Service"
    },
    "5123": {
        "category": "Uncategorized",
        "name": "A configuration entry changed in the OCSP Responder Service"
    },
    "5124": {
        "category": "Uncategorized",
        "name": "A security setting was updated on OCSP Responder Service"
    },
    "5125": {
        "category": "Uncategorized",
        "name": "A request was submitted to OCSP Responder Service"
    },
    "5126": {
        "category": "Uncategorized",
        "name": "Signing Certificate was automatically updated by the OCSP Responder Service"
    },
    "5127": {
        "category": "Uncategorized",
        "name": "The OCSP Revocation Provider successfully updated the revocation information"
    },
    "5136": {
        "category": "Directory Services",
        "name": "A directory service object was modified"
    },
    "5137": {
        "category": "Directory Services",
        "name": "A directory service object was created"
    },
    "5138": {
        "category": "Directory Services",
        "name": "A directory service object was undeleted"
    },
    "5139": {
        "category": "Directory Services",
        "name": "A directory service object was moved"
    },
    "5140": {
        "category": "Object Access",
        "name": "A network share object was accessed"
    },
    "5141": {
        "category": "Directory Services",
        "name": "A directory service object was deleted"
    },
    "5142": {
        "category": "Object Access",
        "name": "A network share object was added."
    },
    "5143": {
        "category": "Object Access",
        "name": "A network share object was modified"
    },
    "5144": {
        "category": "Object Access",
        "name": "A network share object was deleted."
    },
    "5145": {
        "category": "Object Access",
        "name": "A network share object was checked to see whether client can be granted desired access"
    },
    "5146": {
        "category": "System",
        "name": "The Windows Filtering Platform has blocked a packet"
    },
    "5147": {
        "category": "System",
        "name": "A more restrictive Windows Filtering Platform filter has blocked a packet"
    },
    "5148": {
        "category": "Object Access",
        "name": "The Windows Filtering Platform has detected a DoS attack and entered a defensive mode; packets associated with this attack will be discarded."
    },
    "5149": {
        "category": "Object Access",
        "name": "The DoS attack has subsided and normal processing is being resumed."
    },
    "5150": {
        "category": "Object Access",
        "name": "The Windows Filtering Platform has blocked a packet."
    },
    "5151": {
        "category": "Object Access",
        "name": "A more restrictive Windows Filtering Platform filter has blocked a packet."
    },
    "5152": {
        "category": "Object Access",
        "name": "The Windows Filtering Platform blocked a packet"
    },
    "5153": {
        "category": "Object Access",
        "name": "A more restrictive Windows Filtering Platform filter has blocked a packet"
    },
    "5154": {
        "category": "Object Access",
        "name": "The Windows Filtering Platform has permitted an application or service to listen on a port for incoming connections"
    },
    "5155": {
        "category": "Object Access",
        "name": "The Windows Filtering Platform has blocked an application or service from listening on a port for incoming connections"
    },
    "5156": {
        "category": "Object Access",
        "name": "The Windows Filtering Platform has allowed a connection"
    },
    "5157": {
        "category": "Object Access",
        "name": "The Windows Filtering Platform has blocked a connection"
    },
    "5158": {
        "category": "Object Access",
        "name": "The Windows Filtering Platform has permitted a bind to a local port"
    },
    "5159": {
        "category": "Object Access",
        "name": "The Windows Filtering Platform has blocked a bind to a local port"
    },
    "5168": {
        "category": "Object Access",
        "name": "Spn check for SMB/SMB2 fails."
    },
    "5169": {
        "category": "Directory Services",
        "name": "A directory service object was modified"
    },
    "5170": {
        "category": "Directory Services",
        "name": "A directory service object was modified during a background cleanup task"
    },
    "5376": {
        "category": "Account Management",
        "name": "Credential Manager credentials were backed up"
    },
    "5377": {
        "category": "Account Management",
        "name": "Credential Manager credentials were restored from a backup"
    },
    "5378": {
        "category": "Logon Logoff",
        "name": "The requested credentials delegation was disallowed by policy"
    },
    "5379": {
        "category": "System",
        "name": "Credential Manager credentials were read"
    },
    "5380": {
        "category": "System",
        "name": "Vault Find Credential"
    },
    "5381": {
        "category": "System",
        "name": "Vault credentials were read"
    },
    "5382": {
        "category": "System",
        "name": "Vault credentials were read"
    },
    "5440": {
        "category": "Policy Change",
        "name": "The following callout was present when the Windows Filtering Platform Base Filtering Engine started"
    },
    "5441": {
        "category": "Policy Change",
        "name": "The following filter was present when the Windows Filtering Platform Base Filtering Engine started"
    },
    "5442": {
        "category": "Policy Change",
        "name": "The following provider was present when the Windows Filtering Platform Base Filtering Engine started"
    },
    "5443": {
        "category": "Policy Change",
        "name": "The following provider context was present when the Windows Filtering Platform Base Filtering Engine started"
    },
    "5444": {
        "category": "Policy Change",
        "name": "The following sub-layer was present when the Windows Filtering Platform Base Filtering Engine started"
    },
    "5446": {
        "category": "Policy Change",
        "name": "A Windows Filtering Platform callout has been changed"
    },
    "5447": {
        "category": "Policy Change",
        "name": "A Windows Filtering Platform filter has been changed"
    },
    "5448": {
        "category": "Policy Change",
        "name": "A Windows Filtering Platform provider has been changed"
    },
    "5449": {
        "category": "Policy Change",
        "name": "A Windows Filtering Platform provider context has been changed"
    },
    "5450": {
        "category": "Policy Change",
        "name": "A Windows Filtering Platform sub-layer has been changed"
    },
    "5451": {
        "category": "Logon Logoff",
        "name": "An IPsec Quick Mode security association was established"
    },
    "5452": {
        "category": "Logon Logoff",
        "name": "An IPsec Quick Mode security association ended"
    },
    "5453": {
        "category": "Logon Logoff",
        "name": "An IPsec negotiation with a remote computer failed because the IKE and AuthIP IPsec Keying Modules (IKEEXT) service is not started"
    },
    "5456": {
        "category": "Policy Change",
        "name": "PAStore Engine applied Active Directory storage IPsec policy on the computer"
    },
    "5457": {
        "category": "Policy Change",
        "name": "PAStore Engine failed to apply Active Directory storage IPsec policy on the computer"
    },
    "5458": {
        "category": "Policy Change",
        "name": "PAStore Engine applied locally cached copy of Active Directory storage IPsec policy on the computer"
    },
    "5459": {
        "category": "Policy Change",
        "name": "PAStore Engine failed to apply locally cached copy of Active Directory storage IPsec policy on the computer"
    },
    "5460": {
        "category": "Policy Change",
        "name": "PAStore Engine applied local registry storage IPsec policy on the computer"
    },
    "5461": {
        "category": "Policy Change",
        "name": "PAStore Engine failed to apply local registry storage IPsec policy on the computer"
    },
    "5462": {
        "category": "Policy Change",
        "name": "PAStore Engine failed to apply some rules of the active IPsec policy on the computer"
    },
    "5463": {
        "category": "Policy Change",
        "name": "PAStore Engine polled for changes to the active IPsec policy and detected no changes"
    },
    "5464": {
        "category": "Policy Change",
        "name": "PAStore Engine polled for changes to the active IPsec policy, detected changes, and applied them to IPsec Services"
    },
    "5465": {
        "category": "Policy Change",
        "name": "PAStore Engine received a control for forced reloading of IPsec policy and processed the control successfully"
    },
    "5466": {
        "category": "Policy Change",
        "name": "PAStore Engine polled for changes to the Active Directory IPsec policy, determined that Active Directory cannot be reached, and will use the cached copy of the Active Directory IPsec policy instead"
    },
    "5467": {
        "category": "Policy Change",
        "name": "PAStore Engine polled for changes to the Active Directory IPsec policy, determined that Active Directory can be reached, and found no changes to the policy"
    },
    "5468": {
        "category": "Policy Change",
        "name": "PAStore Engine polled for changes to the Active Directory IPsec policy, determined that Active Directory can be reached, found changes to the policy, and applied those changes"
    },
    "5471": {
        "category": "Policy Change",
        "name": "PAStore Engine loaded local storage IPsec policy on the computer"
    },
    "5472": {
        "category": "Policy Change",
        "name": "PAStore Engine failed to load local storage IPsec policy on the computer"
    },
    "5473": {
        "category": "Policy Change",
        "name": "PAStore Engine loaded directory storage IPsec policy on the computer"
    },
    "5474": {
        "category": "Policy Change",
        "name": "PAStore Engine failed to load directory storage IPsec policy on the computer"
    },
    "5477": {
        "category": "Policy Change",
        "name": "PAStore Engine failed to add quick mode filter"
    },
    "5478": {
        "category": "System",
        "name": "IPsec Services has started successfully"
    },
    "5479": {
        "category": "System",
        "name": "IPsec Services has been shut down successfully"
    },
    "5480": {
        "category": "System",
        "name": "IPsec Services failed to get the complete list of network interfaces on the computer"
    },
    "5483": {
        "category": "System",
        "name": "IPsec Services failed to initialize RPC server. IPsec Services could not be started"
    },
    "5484": {
        "category": "System",
        "name": "IPsec Services has experienced a critical failure and has been shut down"
    },
    "5485": {
        "category": "System",
        "name": "IPsec Services failed to process some IPsec filters on a plug-and-play event for network interfaces"
    },
    "5632": {
        "category": "Logon Logoff",
        "name": "A request was made to authenticate to a wireless network"
    },
    "5633": {
        "category": "Logon Logoff",
        "name": "A request was made to authenticate to a wired network"
    },
    "5712": {
        "category": "Process Tracking",
        "name": "A Remote Procedure Call (RPC) was attempted"
    },
    "5888": {
        "category": "Object Access",
        "name": "An object in the COM+ Catalog was modified"
    },
    "5889": {
        "category": "Object Access",
        "name": "An object was deleted from the COM+ Catalog"
    },
    "5890": {
        "category": "System",
        "name": "An object was added to the COM+ Catalog"
    },
    "6144": {
        "category": "Policy Change",
        "name": "Security policy in the group policy objects has been applied successfully"
    },
    "6145": {
        "category": "Policy Change",
        "name": "One or more errors occured while processing security policy in the group policy objects"
    },
    "6272": {
        "category": "Logon Logoff",
        "name": "Network Policy Server granted access to a user"
    },
    "6273": {
        "category": "Logon Logoff",
        "name": "Network Policy Server denied access to a user"
    },
    "6274": {
        "category": "Logon Logoff",
        "name": "Network Policy Server discarded the request for a user"
    },
    "6275": {
        "category": "Logon Logoff",
        "name": "Network Policy Server discarded the accounting request for a user"
    },
    "6276": {
        "category": "Logon Logoff",
        "name": "Network Policy Server quarantined a user"
    },
    "6277": {
        "category": "Logon Logoff",
        "name": "Network Policy Server granted access to a user but put it on probation because the host did not meet the defined health policy"
    },
    "6278": {
        "category": "Logon Logoff",
        "name": "Network Policy Server granted full access to a user because the host met the defined health policy"
    },
    "6279": {
        "category": "Logon Logoff",
        "name": "Network Policy Server locked the user account due to repeated failed authentication attempts"
    },
    "6280": {
        "category": "Logon Logoff",
        "name": "Network Policy Server unlocked the user account"
    },
    "6281": {
        "category": "System",
        "name": "Code Integrity determined that the page hashes of an image file are not valid..."
    },
    "6400": {
        "category": "System",
        "name": "BranchCache: Received an incorrectly formatted response while discovering availability of content."
    },
    "6401": {
        "category": "System",
        "name": "BranchCache: Received invalid data from a peer. Data discarded."
    },
    "6402": {
        "category": "System",
        "name": "BranchCache: The message to the hosted cache offering it data is incorrectly formatted."
    },
    "6403": {
        "category": "System",
        "name": "BranchCache: The hosted cache sent an incorrectly formatted response to the client's message to offer it data."
    },
    "6404": {
        "category": "System",
        "name": "BranchCache: Hosted cache could not be authenticated using the provisioned SSL certificate."
    },
    "6405": {
        "category": "System",
        "name": "BranchCache: instance(s) of event id occurred."
    },
    "6406": {
        "category": "System",
        "name": "registered to Windows Firewall to control filtering for the following:"
    },
    "6408": {
        "category": "System",
        "name": "Registered product failed and Windows Firewall is now controlling the filtering"
    },
    "6409": {
        "category": "System",
        "name": "BranchCache: A service connection point object could not be parsed"
    },
    "6410": {
        "category": "System",
        "name": "Code integrity determined that a file does not meet the security requirements to load into a process. This could be due to the use of shared sections or other issues"
    },
    "6416": {
        "category": "Process Tracking",
        "name": "A new external device was recognized by the system."
    },
    "6417": {
        "category": "System",
        "name": "The FIPS mode crypto selftests succeeded"
    },
    "6418": {
        "category": "System",
        "name": "The FIPS mode crypto selftests failed"
    },
    "6419": {
        "category": "Process Tracking",
        "name": "A request was made to disable a device"
    },
    "6420": {
        "category": "Process Tracking",
        "name": "A device was disabled"
    },
    "6421": {
        "category": "Process Tracking",
        "name": "A request was made to enable a device"
    },
    "6422": {
        "category": "Process Tracking",
        "name": "A device was enabled"
    },
    "6423": {
        "category": "Process Tracking",
        "name": "The installation of this device is forbidden by system policy"
    },
    "6424": {
        "category": "Process Tracking",
        "name": "The installation of this device was allowed, after having previously been forbidden by policy"
    },
    "8191": {
        "category": "System",
        "name": "Highest System-Defined Audit Message Value"
    }
}

import sys
from evtx import PyEvtxParser
import json
import flatten_json
from io import StringIO
import requests
import string
import datetime

headers = {
    "Authorization": api_key,
    "Content-Type": "text/plain"
}


def apiquery(api_post, api_events, global_payload, total_events, nbr_lines):
	try:
		res = requests.post(url=api_url, headers=headers, data=global_payload)
		res.raise_for_status()
	except requests.exceptions.HTTPError as err:
		raise SystemExit(err)
		exit(-2)
	except requests.exceptions.ConnectionError as err:
		raise SystemExit(err)
		exit(-2)
	if DEBUG:
		print("INFO - API POST #%d including %d events / payload size: %.1f KB / %d events uploaded out of %d - %.2f%% / return code:  %s / return output: %s" \
			% (api_post, api_events, len(global_payload)/1024, total_events, nbr_lines, total_events/nbr_lines*100, res, res.text))
	else:
		print("INFO - API POST #%d including %d events / %.2f%% / API POST return --> %s / %s" \
			% (api_post, api_events, total_events/nbr_lines*100, res, res.text), end = '\r', flush=True)


# --- MAIN ---

print("---------------------------------------------")

if api_key == "" or api_url == "":
	print("ERROR - Please specify directly in the script your HTTP log collector url and token key.")
	exit(-1)

if len(sys.argv) == 2:
	file = str(sys.argv[1])
else:
	print("ERROR - Please provide as single parameter the name of the EVTX file you want to import in your XDR instance.")
	exit(-1)

try:
    f = open(file)
except IOError:
    print("ERROR - Your file does not exist or is not accessible")
    exit(-1)
f.close()

print("- CORTEX XDR EVTX file importer script v%s -" % VERSION)
print("- %s" % GIT)
print("---------------------------------------------\n")
if DEBUG:
	print("INFO - DEBUG mode ON")
	print("INFO - %s entries in the eventID mapping table" % len(eventid))
else:
	print("INFO - DEBUG mode OFF")
print("INFO - EVTX file %s analysis in progress" % file)
nbr_lines = 0
first_parser = PyEvtxParser(file)
for line in first_parser.records_json():
	nbr_lines += 1
print("INFO - %d events included in this EVTX file" % nbr_lines)

parser = PyEvtxParser(file)
global_payload = ""

start = datetime.datetime.now()
print("INFO - Import started at %s with %s events per API call\n" % (start.strftime("%Y-%m-%d %H:%M:%S"), api_block_size))

count = 1
api_post = 1
total_events = 0

for record in parser.records_json():
	flat = flatten_json.flatten(json.loads(record['data']), '_')
	try:
		current_evt_id = str(flat["Event_System_EventID"])
		flat["Event_System_EventID_Name"] = eventid[current_evt_id]["name"]
		flat["Event_System_EventID_Type"] = eventid[current_evt_id]["category"]
	except KeyError:
		print("INFO - Missing text description for EventID %s in matching table" % current_evt_id)
		pass
	payload = json.dumps(flat, separators=(',', ':'), sort_keys=True)

	global_payload = global_payload + str(payload) + '\n'
	
	if ((count % api_block_size) == 0):
		api_events = global_payload.count('\n')
		total_events += api_events
		apiquery(api_post, api_events, global_payload, total_events, nbr_lines)
		global_payload = ""
		count = 1
		api_post += 1
	else:
		count += 1

api_events = global_payload.count('\n')
total_events += api_events
apiquery(api_post, api_events, global_payload, total_events, nbr_lines)

stop = datetime.datetime.now()
print("\nINFO - Import finished at %s" % stop.strftime("%Y-%m-%d %H:%M:%S"))

timediff = stop - start
print("INFO - EVTX import in XDR performed with success: %d events imported in %s (hh:mm:ss) at %.2f events/second." \
			% (total_events, timediff, total_events/timediff.seconds))
print("---------------------------------------------")


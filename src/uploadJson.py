from firebase_admin import delete_app
from src.config import FIREBASE_SERVICE_KEY

def authFirebase():
    '''
    Returns db instance for api calls
    Requires service key JSON from google cloud platform in parent directory
    Documentation:
    Saving Data: https://firebase.google.com/docs/database/admin/save-data
    Retrieving Data: https://firebase.google.com/docs/database/admin/retrieve-data
    '''

    import firebase_admin
    from firebase_admin import credentials, db
    import json

    #Key created on google cloud platform
    #https://console.cloud.google.com/iam-admin/serviceaccounts/details/106834063605083129956?authuser=0&project=cfc-gcfd
    params = {
        "databaseURL":'https://cfc-gcfd-default-rtdb.firebaseio.com',
        'databaseAuthBariableOverride': {
            'uid':'my-service-worker'
        }
    }
    #breakpoint()
    try:
        service_key = json.loads(FIREBASE_SERVICE_KEY)
    except:
        service_key = FIREBASE_SERVICE_KEY

    cred = credentials.Certificate(service_key)
    try:
        app = firebase_admin.initialize_app(cred, params)
    except:
        print("App already exists")

    return db


    #references entire db
    #ref = db.reference()
    
    #Returns Cook County Data
    # cook = db.reference('/countyData/17031')
    # print(cook.get())
    
    #test post
    #push generates random key, not sure if this will be a problem
#     alan_dict = {"test": {"alanisawesome": {
#         "date_of_birth": "June 23, 1912",
#         "full_name": "Alan Turing"
#     }
#   }
# }
#     ref.push(alan_dict)
import requests

def toFirebase():
    #load json

    fb = 'https://cfc-gcfd-default-rtdb.firebaseio.com/.json'
    #add authentication token
    
    #delete then put?
    r = requests.post()


def authFirebase():
    import firebase_admin
    from firebase_admin import credentials, db
    
    #Key created on google cloud platform
    #https://console.cloud.google.com/iam-admin/serviceaccounts/details/106834063605083129956?authuser=0&project=cfc-gcfd
    serviceKey = '../cfc-gcfd-ef48601756a7.json'
    params = {
        "databaseURL":'https://cfc-gcfd-default-rtdb.firebaseio.com',
        'databaseAuthBariableOverride': {
            'uid':'my-service-worker'
        }
    }
    #breakpoint()
    cred = credentials.Certificate(serviceKey)
    app = firebase_admin.initialize_app(cred, params)
    
    return db


    #ref entire db
    #ref = db.reference()
    
    # cook = db.reference('/countyData/17031')
    # print(cook.get())
    #post/push to reference
    #https://firebase.google.com/docs/database/admin/save-data
    #print(ref.get('/countyData/17031'))
    
    #test post
    #push generates random key, not sure if this will be a problem
#     alan_dict = {"test": {"alanisawesome": {
#         "date_of_birth": "June 23, 1912",
#         "full_name": "Alan Turing"
#     }
#   }
# }
#     ref.push(alan_dict)
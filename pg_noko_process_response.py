#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# version ='1.0'
# Accepts a response block from a Noko Entries API call and processes the records for loading into DB tables.
# ---------------------------------------------------------------------------
def process_response(response):
    data = response.json()
    strOutline = ""
    for jline in data:
        # record id
        strOutline  = strOutline + str(jline['id'])
        # user
        strOutline = strOutline + ',' + jline['user']['email']
        # Date
        strOutline = strOutline + ',' + str(jline['date'])
        # minutes
        strOutline = strOutline + ',' + str(jline['minutes'])
        # description
        strOutline  = strOutline + ','+jline['description'].replace(",","")
        try:
            #print(jline['project']['name'])
            strOutline = strOutline + ',' + jline['project']['name']
        except:
            strOutline = strOutline + ',' +"N/A"
        if len(strOutline.strip()) > 0:
            strOutline = strOutline.replace('\r', '')
            strOutline = strOutline.replace('\n', '')
            print (strOutline.upper())
        strOutline=""

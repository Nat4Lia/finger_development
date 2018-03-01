import requests
from Send_Error import send_error
import time
import xml.etree.ElementTree as ET
import json
import logging
import instansi_id

logging.basicConfig(filename='FINGERLIBERROR.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

# import lcd_ as cetak

get = {
        'GetAttLog'         : '<GetAttLog><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN></Arg></GetAttLog>',
        'GetUserTemplate'   : '<GetUserTemplate><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN><FingerID xsi:type=\"xsd:integer\">%s</FingerID></Arg></GetUserTemplate>',
        'GetUserInfo'       : '<GetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN Xsi:type=\"xsd:integer\">%s</PIN></Arg></GetUserInfo>',
        'SetUserInfo'       : '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN></PIN><Name>%s</Name><Password></Password><Group></Group><Privilege></Privilege><Card></Card><PIN2>%s</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>',
        'DeleteUser'        : '<DeleteUser><ArgComKey Xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN Xsi:type=\"xsd:integer\">%s</PIN></Arg></DeleteUser>',
        'GetAllUserInfo'    : '<GetAllUserInfo><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey></GetAllUserInfo>',
        'SetUserTemplate'   : '<SetUserTemplate><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN><FingerID xsi:type=\"xsd:integer\">%s</FingerID><Size>%s</Size><Valid>%s</Valid><Template>%s</Template></Arg></SetUserTemplate>',
        'ClearData'         : '<ClearData><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><Value xsi:type=\"xsd:integer\">%s</Value></Arg></ClearData>',
        'GetOption'         : '<GetOption><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><Name xsi:type=\"xsd:string\">%s</Name></Arg></GetOption>',
        'DeleteTemplate'    : '<DeleteTemplate><ArgComKey xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">%s</PIN></Arg></DeleteTemplate>',
        'SetAdminUser'      : '<SetUserInfo><ArgComKey Xsi:type=\"xsd:integer\">%s</ArgComKey><Arg><PIN></PIN><Name>%s</Name><Password></Password><Group></Group><Privilege>14</Privilege><Card></Card><PIN2>%s</PIN2><TZ1></TZ1><TZ2></TZ2><TZ3></TZ3></Arg></SetUserInfo>'
      }

class METHOD:
    def __init__(self):
        self.Header = {'Content-Type' : 'text/xml'}
        self.comKey = 0

    def POST(self, IP_Address, Payload, Timeout=None):
        try:
            r = requests.post('http://%s:80/iWsService' % IP_Address, headers=self.Header, data=Payload, timeout=Timeout)
            print len(ET.fromstring(r.content))
            return ET.fromstring(r.content)
            # return ET.fromstring(r.content)
            # PIN, Name, Password, Group, Privilege, Card, PIN2, TZ0, TZ1, TZ2, TZ3 = [], [], [], [], [], [], [], [], [], [], []
            # for row in root.findall('Row'):
            #     PIN2.append (row.find('PIN').text)
            #     Name.append (row.find('Name').text)
            #     Privilege.append (row.find('Privilege').text)
            # #         PIN.append(data.findall('PIN').text)
            # data = [{'PIN' : pin, 'Name' : name, 'Privilege' : privilege} for pin, name, privilege in zip (PIN2, Name, Privilege)]
            # return json.dumps(data)
            # return None
            # if r.content == 'Successfully':
            #     return True
            # else :
            #     return False
        except (requests.exceptions.RequestException, ET.ParseError, ValueError, TypeError, IndexError)  as err:
            logging.debug(err)
            print 'Fingerprint', err.__class__.__name__
            error       = {'instansi_id' : instansi_id.ID_INSTANSI, 'keterangan' : 'Fingerprint '+IP_Address+' '+err.__class__.__name__}
            send_error(error)
            pass

class finger_command(METHOD):
    def __init__(self, IP_Address):
        METHOD.__init__(self)
        self.IP_Address = IP_Address

    def Option(self,option):
        payload = get['GetOption'] % (self.comKey, option)
        return self.POST (self.IP_Address, payload)
    
    def GetAttLog(self,pin='All'):
        payload = get['GetAttLog'] % (self.comKey, pin)
        return self.POST (self.IP_Address, payload)
    
    def GetUserTemplate(self, pin, templateid):
        payload = get['GetUserTemplate'] % (self.comKey, pin, templateid)
        return self.POST (self.IP_Address, payload)

    def GetUserInfo(self, pin):
        payload = get['GetUserInfo'] % (self.comKey, pin)
        return self.POST (self.IP_Address, payload)

    def SetUserInfo(self, nama, pin):
        payload = get['SetUserInfo'] % (self.comKey, nama, pin)
        return self.POST (self.IP_Address, payload)

    def DeleteUser(self, pin):
        payload = get['DeleteUser'] % (self.comKey, pin)
        return self.POST (self.IP_Address, payload)

    def GetAllUserInfo(self):
        payload = get['GetAllUserInfo'] % (self.comKey)
        return self.POST (self.IP_Address, payload)

    def SetUserTemplate(self, pin, fingerid, size, valid, template):
        payload = get['SetUserTemplate'] % (self.comKey, pin, fingerid, size, valid, template)
        return self.POST (self.IP_Address, payload)

    def DeleteTemplate(self, pin):
        payload = get['DeleteTemplate'] % (self.comKey, pin)
        return self.POST (self.IP_Address, payload)

    def SetAdminUser(self, nama, pin):
        payload = get['SetAdminUser'] % (self.comKey, nama, pin)
        return self.POST (self.IP_Address, payload)

    def ClearPegawai(self, clearcode=1):
        payload = get['ClearData'] % (self.comKey, clearcode) #$ClearCode (1=SEMUA, 2=TEMPLATE?, 3=RECORD)
        exe = self.POST (self.IP_Address, payload, 3)
        return
    
    def ClearAbsensi(self, clearcode=3):
        payload = get['ClearData'] % (self.comKey, clearcode) #$ClearCode (1=SEMUA, 2=TEMPLATE?, 3=RECORD)
        exe = self.POST (self.IP_Address, payload)
        return exe
# payload = get['GetUserInfo'] % (0,0)
# final = json.loads(METHOD().POST('10.10.10.10',payload, None))
# if final :
#     print 'Nama     :',final[0]['Name']
#     if final[0]['Privilege'] == str(14):
#         print 'Status   : Admin'
#     elif final[0]['Privilege'] == str(0):
#         print 'Status   : User'
# else:
#     pass

# x = finger_command('10.10.10.10')
# root = x.GetAllUserInfo()
# if root is not None:
#     for row in root.findall('Row'):
#         print row.find('Name').text
# else:
#     print 'Data Tidak Valid'
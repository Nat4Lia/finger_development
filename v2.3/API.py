import time
import requests
from Send_Error import send_error
import json
import socket
import logging
import instansi_id

logging.basicConfig(filename='APIERROR.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

class METHOD:

    def __init__ (self):
        self.URL    =   'http://eabsen.kalselprov.go.id/api/'
        self.Header =   {
                            'Content-Type'  :   'applicetion/json',
                            'Accept'        :   'application/json'
                        }

    def GET(self, URL, Timeout):
        try:
            r = requests.get(self.URL+URL, headers=self.Header, timeout=Timeout)
            if r.status_code == requests.codes.ok:
                Data = json.loads(r.content)
                return Data
            else :
                return None
        except (requests.exceptions.RequestException, ValueError, TypeError)  as err:
            logging.debug(err)
            print err.__class__.__name__
            error = {'instansi_id' : instansi_id.ID_INSTANSI, 'keterangan' : err.__class__.__name__}
            send_error(error)
            pass

    def POST(self, URL, Payload, Timeout):
        try:
            r = requests.post(self.URL+URL, headers=self.Header, json=Payload, timeout=Timeout)
            if r.status_code == requests.codes.ok:
                return True
            else :
                return False
        except (requests.exceptions.RequestException, ValueError, TypeError)  as err:
            logging.debug(err)
            print err.__class__.__name__
            error       = {'instansi_id' : instansi_id.ID_INSTANSI, 'keterangan' : err.__class__.__name__}
            send_error(error)
            pass

class API(METHOD):
    def __init__ (self):
        METHOD.__init__(self)

    def PEGAWAI(self):
        return self.GET('cekpegawai/%s' % instansi_id.ID_INSTANSI, None)

    def TEMPLATE(self, pegawai_id):
        return self.GET('ambilfinger/%s' %pegawai_id, None)

    def TRIGGER(self):
        trigger = self.GET('triger', None)
        if trigger is not None:
            return trigger[0]['status']
        else:
            return trigger

    def ADMIN(self):
        return self.GET('admin/finger/', None)

    def VERSI(self):
        return self.GET('version', None)

    def MACADDRESS(self):
        return self.GET('macaddress', None)

    def HAPUS_PEGAWAI(self):
        return self.GET('hapusfingerpegawai', None)

    def LOG_RASPBERRY(self, payload):
        return self.POST('lograspberry', payload, None)

    def KEHADIRAN(self, payload):
        return self.POST('attendance', payload, None)

    def LOG_ERROR(self, payload):
        return self.POST('historycrash', payload, None)

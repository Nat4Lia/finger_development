
import xml.etree.ElementTree as ET
import FingerCommandLib as FC
from API import API
import json
import time

class Command:
    def __init__ (self, IP_Address):
        self.IP_Address = IP_Address
        self.do = FC.finger_command(IP_Address)
    #Fungsi Hapus Semua
    def hapussemua (self):
        hasil = False
        try:
            deleteAbsensi = self.do.ClearAbsensi()
            deletePegawai = self.do.ClearPegawai()
            if deleteAbsensi is not None and deletePegawai is None:
            #wait for reset
                print 'Waiting Fingerprint To Connect'
                time.sleep(30)
                rootPegawai = self.do.GetAllUserInfo()
                rootAbsensi = self.do.GetAttLog()
                if (rootPegawai is not None) and (rootAbsensi is not None):
                    if len(rootPegawai)==0 and len(rootAbsensi)==0:
                        hasil = True
                else:
                    hasil = False
            else:
                    hasil = False
        finally:
            return hasil

    #Fungsi Ambil Data MAC
    def ambilmacaddress(self):
        hasil = False
        try:
            root = self.do.Option('MAC')
            if root is not None:
                for row in root.findall('Row'):
                    hasil = row.find('Value').text
            else:
                hasil = False
        finally:
            return hasil

    #Fungsi Cek Jumlah Pegawai
    def jumlahpegawai(self):
        hasil = 0
        try:
            root = self.do.GetAllUserInfo()
            if root is not None:
                for row in root.findall('Row'):
                    if str(row.find('Privilege').text) == str(0):
                        hasil +=1
            else:
                hasil = False
        finally:
            return hasil

    #Fungsi Cek Jumlah Admin
    def jumlahadmin(self):
        hasil = 0
        try:
            root = self.do.GetAllUserInfo()
            if root is not None:
                for row in root.findall('Row'):
                    if str(row.find('Privilege').text) == str(14):
                        hasil +=1
            else:
                hasil = False
        finally:
            return hasil

    # Fungsi Cek Pegawai Finger
    def cekpegawai(self, pegawaiid):
        hasil = False
        try:
            root = self.do.GetUserInfo(pegawaiid)
            if root is not None and len(root) is not 0:
                for row in root.findall('Row'):
                    if str(row.find('PIN2').text) == str(pegawaiid):
                        hasil = True
                    else :
                        hasil = False
            else:
                hasil = False
        finally:
            return hasil

    #Fungsi Hapus Pegawai Finger
    def hapuspegawai(self, pegawaiid):
        hasil = False #User Tidak Ada
        try:
            while self.cekpegawai(pegawaiid) :
                root = self.do.DeleteUser(pegawaiid)
                if root is not None:
                    for row in root.findall('Row'):
                        hasil = row.find('Information').text
                else:
                    hasil = False

        finally:
            return hasil
            
    #Fungsi Daftar Pegawai
    def daftarpegawai(self, pegawaiid, nama):
        hasil =False
        status = None
        statusTemplate = []
        try:
            if not self.cekpegawai(pegawaiid):
                #Proses Pendaftaran
                loadtemplate = API().TEMPLATE(pegawaiid)
                rootUser = self.do.SetUserInfo(nama, pegawaiid)
                if rootUser is not None:
                    for row in rootUser.findall('Row'):
                        status = row.find('Information').text
                    if status == 'Successfully!' :
                        for templateid in range (0, len(loadtemplate)):
                            size            = loadtemplate[templateid]['size']
                            valid           = loadtemplate[templateid]['valid']
                            finger_template = loadtemplate[templateid]['templatefinger']
                            rootTemplate    = self.do.SetUserTemplate(pegawaiid, templateid, size, valid, finger_template)
                            if rootTemplate is not None:
                                for row in rootTemplate.findall('Row'):
                                    statusTemplate.append(row.find('Information').text)
                            else:
                                hasil = False
                        if statusTemplate:
                            if statusTemplate[0] == 'Successfully!' and statusTemplate[1] == 'Successfully!':
                                hasil = True
                            else:
                                hasil = False
                        else:
                            hasil = False
                else:
                    hasil = False
            else:
                hasil = True
        finally:
            if hasil :
                return hasil
            else :
                self.hapuspegawai(pegawaiid)
                return hasil
            
    #Fungsi Daftar Pegawai
    def daftaradmin(self, pegawaiid, nama):
        hasil =False
        status = None
        statusTemplate = []
        try:
            if not self.cekpegawai(pegawaiid):
                #Proses Pendaftaran
                loadtemplate = API().TEMPLATE(pegawaiid)
                rootUser = self.do.SetAdminUser(nama, pegawaiid)
                if rootUser is not None:
                    for row in rootUser.findall('Row'):
                        status = row.find('Information').text
                    if status == 'Successfully!' :
                        for templateid in range (0, len(loadtemplate)):
                            size            = loadtemplate[templateid]['size']
                            valid           = loadtemplate[templateid]['valid']
                            finger_template = loadtemplate[templateid]['templatefinger']
                            rootTemplate    = self.do.SetUserTemplate(pegawaiid, templateid, size, valid, finger_template)
                            if rootTemplate is not None:
                                for row in rootTemplate.findall('Row'):
                                    statusTemplate.append(row.find('Information').text)
                            else:
                                hasil = False
                        if statusTemplate:
                            if statusTemplate[0] == 'Successfully!' and statusTemplate[1] == 'Successfully!':
                                hasil = True
                            else:
                                hasil = False
                        else:
                            hasil = False
                else:
                    hasil = False
            else:
                hasil = True
        finally:
            if hasil :
                return hasil
            else :
                gagal = self.hapuspegawai(pegawaiid)
                return hasil

    # #Fungsi Hapus Data Absensi
    def hapusabsensi(self):
        hasil = False
        try:
            self.do.ClearAbsensi(3)
            rootCheck   = self.do.GetAttLog()
            if rootCheck is not None and len(rootCheck) is 0:
                hasil = True
            else :
                self.hapusabsensi()
        finally:
            return hasil

    #Fungsi Mengambil Data Absensi
    def ambildataabsensi(self):
        hasil = False
        try:
            root    = self.do.GetAttLog()
            if root is not None and len(root) is not 0 :
                PIN, TANGGAL, JAM, STATUS = [], [], [], []
                for row in root.findall('Row'):
                    PIN.append(row.find('PIN').text)
                    TANGGAL.append(row.find('DateTime').text.split()[0])
                    JAM.append(row.find('DateTime').text.split()[1])
                    STATUS.append(row.find('Status').text)
                absensi = [{'PIN'       : pin,
                            'Tanggal'   : tanggal,
                            'Jam'       : jam,
                            'Status'    : status} for pin, tanggal, jam, status in zip (PIN, TANGGAL, JAM, STATUS)]
                hasil = json.loads(json.dumps(absensi))
            else:
                hasil = False
        finally:
            return hasil

    #Fungsi Mengambil semua data pegawai
    def semuadatapegawai(self):
        hasil = False
        try:
            root = self.do.GetAllUserInfo()
            if root is not None and len(root) is not 0:
                PIN, Name, Password, Group, Privilege, Card, PIN2, TZ0, TZ1, TZ2, TZ3 = [], [], [], [], [], [], [], [], [], [], []
                for row in root.findall('Row'):
                    if str(row.find('Privilege').text) == str(0):
                        PIN2.append (row.find('PIN2').text)
                        Name.append (row.find('Name').text)
                        Privilege.append (row.find('Privilege').text)
                data = [{'PIN' : pin, 'Name' : name, 'Privilege' : privilege} for pin, name, privilege in zip (PIN2, Name, Privilege)]
                hasil = json.loads(json.dumps(data))
            else:
                hasil = False
        finally:
            return hasil

    #Fungsi Mengambil semua data pegawai
    def semuadataadmin(self):
        hasil = False
        try:
            root = self.do.GetAllUserInfo()
            if root is not None and len(root) is not 0:
                PIN, Name, Password, Group, Privilege, Card, PIN2, TZ0, TZ1, TZ2, TZ3 = [], [], [], [], [], [], [], [], [], [], []
                for row in root.findall('Row'):
                    if str(row.find('Privilege').text) == str(14):
                        PIN2.append (row.find('PIN2').text)
                        Name.append (row.find('Name').text)
                        Privilege.append (row.find('Privilege').text)
                data = [{'PIN' : pin, 'Name' : name, 'Privilege' : privilege} for pin, name, privilege in zip (PIN2, Name, Privilege)]
                hasil = json.loads(json.dumps(data))
            else:
                hasil = False
        finally:
            return hasil
# print daftarpegawai('Finger A','10.10.10.10:80',15,'FAHRUL')
# print cekpegawai('Finger A','10.10.10.10:80',15)
# hapuspegawai('Finger', '10.10.10.10:80', 15)
# print jumlahpegawai('Finger', '10.10.10.10:80')
# print semuadatapegawai('Finger', '10.10.10.10:80')[0][4].text
# print hapussemua('Finger A','10.10.10.10')

# print Command('10.10.10.10').hapuspegawai(7239)
# print Command('10.10.10.10').semuadatapegawai()

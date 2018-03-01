import xml.etree.ElementTree as ET
import FingerCommandLib as FC
from API import API
import json
import time

class Command:
    def __init__ (self, IP_Address):
        self.do = FC.finger_command(IP_Address)
    #Fungsi Hapus Semua
    def hapussemua (self):
        deleteAbsensi = self.do.ClearAbsensi()
        deletePegawai = self.do.ClearPegawai()
        #wait for reset
        print 'Waiting Fingerprint To Connect'
        time.sleep(30)
        rootPegawai = self.do.GetAllUserInfo()
        rootAbsensi = self.do.GetAttLog()
        if len(rootPegawai)==0 and len(rootAbsensi)==0:
            return 'Complete'
        else:
            return 'Failed'

    #Fungsi Ambil Data MAC
    def ambilmacaddress(self):
        root = self.do.Option('MAC')
        if root is not None:
            for row in root.findall('Row'):
                return row.find('Value').text
        else:
            return 'Data Tidak Valid'

    #Fungsi Cek Jumlah Pegawai
    def jumlahpegawai(self):
        root = self.do.GetAllUserInfo()
        if root is not None:
            jumlah = 0
            for row in root.findall('Row'):
                if str(row.find('Privilege').text) == str(0):
                    jumlah +=1
            return jumlah
        else:
            return 'Data Tidak Valid'

    #Fungsi Cek Jumlah Admin
    def jumlahpegawai(self):
        root = self.do.GetAllUserInfo()
        if root is not None:
            jumlah = 0
            for row in root.findall('Row'):
                if str(row.find('Privilege').text) == str(14):
                    jumlah +=1
            return jumlah
        else:
            return 'Data Tidak Valid'

    # Fungsi Cek Pegawai Finger
    def cekpegawai(self, pegawaiid):
        root = self.do.GetUserInfo(pegawaiid)
        if root is not None and len(root) is not 0:
            for row in root.findall('Row'):
                if str(row.find('PIN2').text) == str(pegawaiid):
                    return True
                else :
                    return False
        else:
            return False

    #Fungsi Hapus Pegawai Finger
    def hapuspegawai(self, pegawaiid):
        status = None #User Tidak Ada = None
        while self.cekpegawai(pegawaiid) :
            root = self.do.DeleteUser(pegawaiid)
            if root is not None:
                for row in root.findall('Row'):
                    status = row.find('Information').text
            else:
                return 'Data Tidak Valid'
        else:
            return status
            
    #Fungsi Daftar Pegawai
    def daftarpegawai(self, pegawaiid, nama):
        status = None
        statusTemplate = None
        while not self.cekpegawai(pegawaiid):
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
                                statusTemplate = row.find('Information').text
                        else:
                            gagal = self.hapuspegawai(pegawaiid)
                            return 'Daftar Gagal'
            else:
                return 'Daftar Gagal'
        else:
            return status

    #Fungsi Daftar Pegawai
    def daftaradmin(self, pegawaiid, nama):
        status = None
        statusTemplate = None
        while not self.cekpegawai(pegawaiid):
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
                                statusTemplate = row.find('Information').text
                        else:
                            gagal = self.hapuspegawai(pegawaiid)
                            return 'Daftar Gagal'
            else:
                return 'Daftar Gagal'
        else:
            return status

    # #Fungsi Hapus Data Absensi
    def hapusabsensi(self):
        rootData    = self.do.ClearData(3)
        rootCheck   = self.do.GetAttLog()
        if rootCheck is not None and len(rootCheck) is 0:
            return 'Success'
        else :
            self.hapusabsensi()

    #Fungsi Mengambil Data Absensi
    def ambildataabsensi(self):
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
            return json.loads(json.dumps(absensi))
        else:
            return 'Data Tidak Valid'
          

    #Fungsi Mengambil semua data pegawai
    def semuadatapegawai(self):
        root = self.do.GetAllUserInfo()
        if root is not None and len(root) is not 0:
            PIN, Name, Password, Group, Privilege, Card, PIN2, TZ0, TZ1, TZ2, TZ3 = [], [], [], [], [], [], [], [], [], [], []
            for row in root.findall('Row'):
                PIN2.append (row.find('PIN').text)
                Name.append (row.find('Name').text)
                Privilege.append (row.find('Privilege').text)
            data = [{'PIN' : pin, 'Name' : name, 'Privilege' : privilege} for pin, name, privilege in zip (PIN2, Name, Privilege)]
            return json.loads(json.dumps(data))
        else:
            return 'Data Tidak Valid'
# print daftarpegawai('Finger A','10.10.10.10:80',15,'FAHRUL')
# print cekpegawai('Finger A','10.10.10.10:80',15)
# hapuspegawai('Finger', '10.10.10.10:80', 15)
# print jumlahpegawai('Finger', '10.10.10.10:80')
# print semuadatapegawai('Finger', '10.10.10.10:80')[0][4].text
# print hapussemua('Finger A','10.10.10.10')

# print Command('10.10.10.10').hapuspegawai(7239)
# print Command('10.10.10.10').semuadatapegawai()

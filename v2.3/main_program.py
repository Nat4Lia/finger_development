from API import API
import Local_Access as Local
from Fingerprint_Access import Command as Finger
import instansi_id
import time
# import lcd_ as cetak
from subprocess import check_call as run
import os
from Request_Retry_Session import requests_retry_session

Localhost   = Local.Localhost()

WebAPI      = API()

def encrypt(data):
    key = 'D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121'
    textASCII = [ord(x) for x in data]
    keyASCII = [ord(x) for x in key]
    encASCII = [(41+((x+y)%26)) for x, y in zip (textASCII, keyASCII)]
    encText = ''.join(chr(x) for x in encASCII)
    return encText
class execution:
    def __init__(self):
        self.trigger = 1#WebAPI.TRIGGER()

    def resetall(self, IP_Address):
        hasil = False
        try:
            if self.trigger is 4 and self.trigger is not None:
                print 'Fingerprint Akan Di Reset'
                if Finger(IP_Address).hapussemua() :
                    hasil = True
                else:
                    hasil = False
            else:
                hasil = False
        finally:
            return hasil


#     if Server.load('Trigger',None) is 4:
#         for alamat in usealamat:
#             cetak.printLCD ('Reset Semua Data','').lcd_status()
#             JUMLAHPEGAWAIFINGER = Finger.jumlahpegawai(alamat, usealamat[alamat])
#             JUMLAHDATAABSENSI   = len(Finger.ambildataabsensi(alamat, usealamat[alamat]))
#             if JUMLAHDATAABSENSI or JUMLAHPEGAWAIFINGER != 0:
#                 Finger.hapusabsensi(alamat, usealamat[alamat])
#                 Finger.hapussemua(alamat, usealamat[alamat])
#                 Localhost.hapussemua()
#                 cetak.printLCD ('Reseting %s' % alamat,'').lcd_status()
#                 time.sleep(30)
    def update(self):
        SRC = '/home/pi/finger'
        CMD = {
                'REMOVESOURCE'  : 'sudo rm -rf %s',
                'CLONETOSOURCE' : 'sudo git clone https://github.com/Nat4Lia/finger.git %s',
                'COPYTOETC'     : 'sudo cp -R /home/pi/finger /etc/',
                'REBOOT'        : 'sudo reboot'
        }

        if self.trigger is 3 and self.trigger is not None :
            version = WebAPI.VERSI()
            if Localhost.cekversion(version) :
                print 'Update'
                if os.path.isdir(SRC) :
                    run(CMD['REMOVESOURCE'] % SRC,shell=True)
                    run(CMD['CLONETOSOURCE'] % SRC,shell=True)
                    run(CMD['COPYTOETC'], shell=True)
                    Localhost.updateversion(version)
                else :
                    run(CMD['CLONETOSOURCE'] % SRC,shell=True)
                    run(CMD['COPYTOETC'], shell=True)
                    Localhost.tambahversion(version)
                print 'update ke versi...'
                time.sleep(5)
                print 'reboot'
                run(CMD['REBOOT'], shell=True)


# def clone():
#     SRC = '/home/pi/finger'
#     CMD = {
#             'REMOVESOURCE'  : 'sudo rm -rf %s',
#             'CLONETOSOURCE' : 'sudo git clone https://github.com/Nat4Lia/finger.git %s',
#             'COPYTOETC'     : 'sudo cp -R /home/pi/finger /etc/',
#             'REBOOT'        : 'sudo reboot'
#     }

#     if Server.load('Trigger',None) is 3 :
#         version = Server.load('Update',None)
#         if Localhost.cekversion(version) :
#             cetak.printLCD ('Updating...','').lcd_status()
#             if os.path.isdir(SRC) :
#                 run(CMD['REMOVESOURCE'] % SRC,shell=True)
#                 run(CMD['CLONETOSOURCE'] % SRC,shell=True)
#                 run(CMD['COPYTOETC'], shell=True)
#                 Localhost.updateversion(version)
#             else :
#                 run(CMD['CLONETOSOURCE'] % SRC,shell=True)
#                 run(CMD['COPYTOETC'], shell=True)
#                 Localhost.tambahversion(version)
#             cetak.printLCD('Update ke versi','%s' % version).lcd_status()
#             time.sleep(5)
#             cetak.printLCD('Restarting Raspberry','...').lcd_status()
#             run(CMD['REBOOT'], shell=True)

    def manajemen_pegawai(self, IP_Address):
        if self.trigger is 1 and self.trigger is not None :
            Mac                     = Finger(IP_Address).ambilmacaddress()
            pegawai_API             = WebAPI.PEGAWAI()
            pegawai_Finger          = Finger(IP_Address).semuadatapegawai()

            # print pegawai_Finger
            
            if Mac and pegawai_API is not None and pegawai_Finger is not None:
                
                jumlah_pegawai_API      = len(pegawai_API)
                jumlah_pegawai_Local    = Localhost.cekjumlahpegawai(Mac)
                jumlah_pegawai_Finger   = Finger(IP_Address).jumlahpegawai()

                if jumlah_pegawai_Finger != jumlah_pegawai_Local or jumlah_pegawai_Finger != jumlah_pegawai_API or jumlah_pegawai_Local != jumlah_pegawai_API:
                    #Sesuaikan data di Finger dan Localhost dengan API
                    for pegawai_di_Finger in pegawai_Finger:
                        for pegawai_di_API in pegawai_API:
                            print pegawai_di_API['pegawai_id'],pegawai_di_Finger['PIN']
                            if str(pegawai_di_API['pegawai_id']) == str(pegawai_di_Finger['PIN']):
                                print 'ok'
                                break
                            else:
                                print 'next'
                        print 'hapus',pegawai_di_Finger['PIN']#,Finger(IP_Address).hapuspegawai(pegawai_di_Finger['PIN']),Localhost.hapuspegawai(pegawai_di_Finger['PIN'], Mac)
                    #Daftarkan Pegawai
                    for pegawai_di_API in pegawai_API:
                        Finger(IP_Address).daftarpegawai(pegawai_di_API['pegawai_id'], pegawai_di_API['nama'].replace("'"," "))
                        Localhost.daftarpegawai(pegawai_di_API['pegawai_id'], pegawai_di_API['nama'].replace("'"," "),Mac)
                else:
                    print 'skip'

            else:
                print False
            

        # print jumlah_pegawai_API, jumlah_pegawai_Local, jumlah_pegawai_Finger
execution().manajemen_pegawai('10.10.10.10')
# def hapuspegawai(tujuan, alamat, pegawaiid, mac):
#     while True:
#         Finger.hapuspegawai(tujuan, alamat, pegawaiid)
#         if not Finger.cekpegawai(tujuan, alamat, pegawaiid) and not Localhost.hapuspegawai(pegawaiid, mac):
#             return True
#         else:
#             return False

# def daftarpegawai(tujuan, alamat, pegawaiid, nama, mac):
#     try:
#         daftarfinger    = Finger.daftarpegawai(tujuan, alamat, pegawaiid, nama)
#         daftarlocal     = Localhost.daftarpegawai(pegawaiid, nama, mac)

#         if daftarfinger and daftarlocal:
#             return 'Sukses'
#         elif daftarfinger and not daftarlocal:
#             return 'Finger'
#         elif not daftarfinger and daftarlocal:
#             return 'Localhost'
#         else:
#             pass
#     except IOError as err:
#         pass

# def normalizepegawai(data, dataapi, tujuan, alamat, mac):
#     #normalise fingerprint ke localhost
#     pegawaifinger = Finger.semuadatapegawai(tujuan, alamat)
#     for pegawai in pegawaifinger:
#         if str(pegawai[4].text) == str(0):
#             if Localhost.cekpegawai(pegawai[6].text, mac) :
#                 pass
#             else:
#                 Finger.hapuspegawai(tujuan, alamat, pegawai[6].text)
#         else:
#             pass

#     #normalise localhost ke API
#     for pegawai in data:
#         status = False
#         normal = Localhost.normalizelocalhostpegawai(pegawai[0], mac)

#         if len(normal) > 1 :
#             Localhost.hapuspegawai(pegawai[0],mac)
#             while True:
#                 if Finger.cekpegawai(tujuan, alamat, pegawai[0]):
#                     Finger.hapuspegawai(tujuan, alamat, pegawai[0])
#                 else:
#                     break
#         else:
#             pass

#         for pegawaiapi in dataapi:
#             if pegawaiapi['id'] == pegawai[0] and Finger.cekpegawai(tujuan, alamat, pegawaiapi['id']):
#                 status = True
#                 break

#         if not status:
#             #hapus pegawai
#             Localhost.hapuspegawai(pegawai[0],mac)
#             while True:
#                 if Finger.cekpegawai(tujuan, alamat, pegawai[0]):
#                     Finger.hapuspegawai(tujuan, alamat, pegawai[0])
#                 else:
#                     break
#         else:
#             pass
#     return

# def hapusadmin(tujuan, alamat, pegawaiid, mac):
#     while True:
#         Finger.hapuspegawai(tujuan, alamat, pegawaiid)
#         if not Finger.cekpegawai(tujuan, alamat, pegawaiid) and not Localhost.hapusadmin(pegawaiid, mac):
#             return True
#         else:
#             return False

# def daftaradmin(tujuan, alamat, adminid, nama, mac):
#     try:
#         daftarfinger    = Finger.daftaradmin(tujuan, alamat, adminid, nama)
#         daftarlocal     = Localhost.daftaradmin(adminid, nama, mac)

#         if daftarfinger and daftarlocal:
#             return 'Sukses'
#         elif daftarfinger and not daftarlocal:
#             return 'Finger'
#         elif not daftarfinger and daftarlocal:
#             return 'Localhost'
#         else:
#             pass
#     except IOError as err:
#         pass

# def normalizeadmin(data, dataapi, tujuan, alamat, mac):
#     #normalise fingerprint ke localhost
#     pegawaifinger = Finger.semuadatapegawai(tujuan, alamat)
#     for pegawai in pegawaifinger:
#         if str(pegawai[4].text) == str(14):
#             if Localhost.cekadmin(pegawai[6].text, mac) :
#                 pass
#             else:
#                 Finger.hapuspegawai(tujuan, alamat, pegawai[6].text)
#         else:
#             pass

#     #normalise localhost ke API
#     for pegawai in data:
#         status = False
#         normal = Localhost.normalizelocalhostpegawai(pegawai[0], mac)

#         if len(normal) > 1 :
#             Localhost.hapusadmin(pegawai[0],mac)
#             while True:
#                 if Finger.cekpegawai(tujuan, alamat, pegawai[0]):
#                     Finger.hapuspegawai(tujuan, alamat, pegawai[0])
#                 else:
#                     break
#         else:
#             pass

#         for pegawaiapi in dataapi:
#             if pegawaiapi['id'] == pegawai[0] and Finger.cekpegawai(tujuan, alamat, pegawaiapi['id']):
#                 status = True
#                 break

#         if not status:
#             #hapus pegawai
#             Localhost.hapusadmin(pegawai[0],mac)
#             while True:
#                 if Finger.cekpegawai(tujuan, alamat, pegawai[0]):
#                     Finger.hapuspegawai(tujuan, alamat, pegawai[0])
#                 else:
#                     break
#         else:
#             pass
#     return

# def normalizemac(datalocal, dataserver):
#     for listmaclocal in range(0,len(datalocal)):
#         try:
#             macL = datalocal[listmaclocal][0]
#             status = False
#             for listmacserver in dataserver:
#                 try:
#                     if macL in listmacserver['macaddress']:
#                         status = macL in listmacserver['macaddress']
#                         break
#                 except TypeError as err:
#                     pass
#                 except IndexError as err:
#                     pass
#                 except ValueError as err:
#                     pass
#             if not status:
#                 Localhost.hapusmac(macL)
#         except TypeError as err:
#             pass
#         except IndexError as err:
#             pass
#         except ValueError as err:
#             pass

# def daftarmac():
#     DAFTARMACADDRESSSERVER  = Server.load('Macaddress',None)
#     JUMLAHMACADDRESSSERVER  = len(DAFTARMACADDRESSSERVER)
#     MACLOCAL                = Localhost.cekkesemuamac()
#     normalizemac(MACLOCAL, DAFTARMACADDRESSSERVER)
#     JUMLAHMACADDRESSLOCAL   = Localhost.cekjumlahmac()
#     SELISIHJUMLAHMAC        = JUMLAHMACADDRESSSERVER - JUMLAHMACADDRESSLOCAL
#     if SELISIHJUMLAHMAC > 0:
#         for DAFTARMAC in range (JUMLAHMACADDRESSLOCAL, JUMLAHMACADDRESSSERVER):
#             try:
#                 MACADDRESS = DAFTARMACADDRESSSERVER[DAFTARMAC]['macaddress']
#                 Localhost.daftarmac(MACADDRESS)
#             except TypeError as err:
#                 pass
#             except IndexError as err:
#                 pass
#             except ValueError as err:
#                 pass

# class Proses:
#     def __init__ (self, tujuan, alamat):
#         self.tujuan = tujuan
#         self.alamat = alamat

#     def manajemenuser(self):
#         tujuan  = self.tujuan
#         alamat  = self.alamat
#         mac     = Finger.ambilmacaddress(tujuan, alamat)
#         jumlahDihapus       = 0
#         if Localhost.macterdaftar(mac) :
#             cetak.printLCD('Pengaturan Pegawai','Fingerprint').lcd_status()
#             if Server.load('Trigger',None) is 1:
#                 APICEKPEGAWAI          = Server.load('Pegawai',instansi_id.ID_INSTANSI)
#                 LOCALHOSTCEKPEGAWAI     = Localhost.carisemuapegawai(mac)
#                 normalizepegawai(LOCALHOSTCEKPEGAWAI, APICEKPEGAWAI, tujuan, alamat, mac)
#                 JUMLAHPEGAWAISERVER     = len(APICEKPEGAWAI)
#                 JUMLAHPEGAWAIFINGER     = Finger.jumlahpegawai(tujuan, alamat) - Localhost.cekjumlahadmin(mac)
#                 JUMMLAHPEGAWAILOCAL     = Localhost.cekjumlahpegawai(mac)
#                 SELISIHJUMLAHPEGAWAI    = JUMLAHPEGAWAISERVER - JUMMLAHPEGAWAILOCAL
#                 JumlahDaftarBaru        = 0
#                 if SELISIHJUMLAHPEGAWAI > 0: #Jika Terdapat Pegawai Baru Di Server
#                     #MENGAMBIL DATA ARRAY API
#                     cetak.printLCD('Menambahkan','Pegawai').lcd_status()
#                     for PEGAWAI in range (0, JUMLAHPEGAWAISERVER):
#                         #Mengambil ID dan NAMA pegawai
#                         try:
#                             ID =  APICEKPEGAWAI[PEGAWAI]['id']
#                             NAMA = APICEKPEGAWAI[PEGAWAI]['nama'].replace("'"," ")
#                         except ValueError as err:
#                             pass
#                         except TypeError as err:
#                             pass
#                         #Daftarkan Pegawai
#                         try:
#                             daftarkan   = daftarpegawai(tujuan, alamat, ID, NAMA, mac)
#                         except IOError as err:
#                             pass
#                 else:
#                     pass

#                 if JumlahDaftarBaru == 0:
#                     pass
#                     cetak.printLCD('Tidak Ada','Pegawai Baru').lcd_status()
#                 else:
#                     pass
#                     cetak.printLCD('%s Pegawai Baru' % JumlahDaftarBaru,'Berhasil Ditambahkan').lcd_status()

#             elif Server.load('Trigger',None) is 2:
#                 APIHAPUSPEGAWAI         = Server.load('HapusPegawai',None)
#                 JUMLAHPEGAWAIDIHAPUS    = len(APIHAPUSPEGAWAI)
#                 for PEGAWAI in range (0, JUMLAHPEGAWAIDIHAPUS) :
#                     try:
#                         ID      = APIHAPUSPEGAWAI[PEGAWAI]['pegawai_id']
#                         hapuspegawai(tujuan,  alamat, ID, mac)
#                         jumlahDihapus += 1
#                     except ValueError as err:
#                         pass
#                     except TypeError as err:
#                         pass

#                 cetak.printLCD('%s Pegawai' % JumlahDaftarBaru,'Berhasil Dihapus').lcd_status()


#         else:
#             cetak.printLCD('Mac Fingerprint','Tidak Terdaftar').lcd_status()
#             time.sleep(3)
#             cetak.printLCD('Hubungi Kominfo','Untuk Mendaftarkan').lcd_status()
#             time.sleep(3)

#     def manajemenadmin(self):
#         tujuan  = self.tujuan
#         alamat  = self.alamat
#         mac     = Finger.ambilmacaddress(tujuan, alamat)
#         jumlahDihapus       = 0
#         if Localhost.macterdaftar(mac) :
#             if Server.load('Trigger',None) is 1:
#                 APICEKADMIN             = Server.load('Admin',None)
#                 LOCALHOSTCEKADMIN       = Localhost.carisemuaadmin(mac)
#                 normalizeadmin(LOCALHOSTCEKADMIN, APICEKADMIN, tujuan, alamat, mac)
#                 JUMLAHADMINSERVER       = len(APICEKADMIN)
#                 JUMLAHADMINFINGER       = Finger.jumlahpegawai(tujuan, alamat) - Localhost.cekjumlahpegawai(mac)
#                 JUMMLAHADMINLOCAL       = Localhost.cekjumlahadmin(mac)
#                 SELISIHJUMLAHADMIN      = JUMLAHADMINSERVER - JUMMLAHADMINLOCAL
#                 JumlahDaftarBaru        = 0
#                 if SELISIHJUMLAHADMIN > 0 : #Jika Terdapat ADMIN Baru Di Server
#                     cetak.printLCD('Menambahkan','Admin').lcd_status()
#                     #MENGAMBIL DATA ARRAY API
#                     for ADMIN in range (0, JUMLAHADMINSERVER):
#                         #Mengambil ID dan NAMA ADMIN
#                         try:
#                             ID =  APICEKADMIN[ADMIN]['id']
#                             NAMA = APICEKADMIN[ADMIN]['nama'].replace("'"," ")
#                         except ValueError as err:
#                             pass
#                         except TypeError as err:
#                             pass
#                         #Daftarkan ADMIN
#                         try:
#                             daftarkan   = daftaradmin(tujuan, alamat, ID, NAMA, mac)
#                         except IOError as err:
#                             pass
#                 else:
#                     pass

#                 if JumlahDaftarBaru == 0:
#                     pass
#                     cetak.printLCD('Tidak Ada','Admin Baru').lcd_status()
#                 else:
#                     pass
#                     cetak.printLCD('%s Admin Baru' % JumlahDaftarBaru,'Berhasil Ditambahkan').lcd_status()

#             elif Server.load('Trigger',None) is 2:
#                 APIHAPUSADMIN         = Server.load('Admin',None)
#                 JUMLAHADMINDIHAPUS    = len(APIHAPUSADMIN)
#                 for ADMIN in range (0, JUMLAHADMINDIHAPUS) :
#                     try:
#                         ID      = APIHAPUSADMIN[ADMIN]['pegawai_id']
#                         hapusadmin(tujuan,  alamat, ID, mac)
#                         jumlahDihapus += 1
#                     except ValueError as err:
#                         pass
#                     except TypeError as err:
#                         pass
#                 cetak.printLCD('%s Admin' % JumlahDaftarBaru,'Berhasil Dihapus').lcd_status()
#         else:
#             pass
#             cetak.printLCD('Mac Fingerprint','Tidak Terdaftar').lcd_status()
#             cetak.printLCD('Hubungi Kominfo','Untuk Mendaftarkan').lcd_status()

#     def clearlog(self):
#         tujuan  = self.tujuan
#         alamat  = self.alamat
#         mac     = Finger.ambilmacaddress(tujuan, alamat)

#         if Localhost.macterdaftar(mac) :
#             #Jika Mac Terdaftar
#             JUMLAHABSENSIFINGER     = len(Finger.ambildataabsensi(tujuan, alamat))
#             JUMLAHABSENSILOCAL      = Localhost.cekjumlahabsensi(mac)
#             if (JUMLAHABSENSIFINGER and JUMLAHABSENSILOCAL) >=50000:
#                 cetak.printLCD('Menghapus data','absensi lama').lcd_status()
#                 Finger.hapusabsensi(tujuan, alamat)
#                 Localhost.hapusdataabsensi(mac)
#         else:
#             cetak.printLCD('Mac Fingerprint','Tidak Terdaftar').lcd_status()
#             time.sleep(3)
#             cetak.printLCD('Hubungi Kominfo','Untuk Mendaftarkan').lcd_status()
#             time.sleep(3)


#     def kirimdataabsensi(self):
#         tujuan  = self.tujuan
#         alamat  = self.alamat
#         mac     = Finger.ambilmacaddress(tujuan, alamat)

#         if Localhost.macterdaftar(mac) :
#             cetak.printLCD('Mengambil Data','Absensi').lcd_status()
#             DATAABSENSI             = Finger.ambildataabsensi(tujuan, alamat)
#             JUMLAHDATAABSENSI       = len(DATAABSENSI)
#             JUMLAHDATAABSENSILOCAL  = Localhost.cekjumlahabsensi(mac)
#             SELISIHDATAABSENSI      = JUMLAHDATAABSENSI - JUMLAHDATAABSENSILOCAL
#             TOTALSUKSESPOST         = 0
#             TOTALGAGALPOST          = 0
#             if SELISIHDATAABSENSI > 0:
#                 for DATA in range (JUMLAHDATAABSENSILOCAL, JUMLAHDATAABSENSI):
#                     try:
#                         IDINSTANSI      = instansi_id.ID_INSTANSI
#                         USERPIN         = DATAABSENSI[DATA][0].text
#                         TANGGAL, JAM    = DATAABSENSI[DATA][1].text.split(' ')
#                         VERIFIKASI      = DATAABSENSI[DATA][2].text
#                         STATUS          = DATAABSENSI[DATA][3].text
#                         MACADDRESS      = mac

#                         encryptText     = str(JAM) + str(TANGGAL) + str(USERPIN) + str(IDINSTANSI) + str(STATUS)
#                         encryption      = encrypt(encryptText)

#                         headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
#                         payload = {'status' : STATUS, 'instansi' : IDINSTANSI, 'jam' : JAM, 'tanggal' : TANGGAL, 'user_id' : USERPIN, 'token' : encryption }

#                         if Server.POST('KEHADIRAN', headers, payload):
#                             Localhost.inputdataabsensi(USERPIN, MACADDRESS)
#                             TOTALSUKSESPOST +=1
#                             cetak.printLCD('Total Absensi','Berhasil Dikirim %s' % TOTALSUKSESPOST).lcd_status()
#                         else:
#                             TOTALGAGALPOST +=1
#                             cetak.printLCD('Total Absensi','Gagal Dikirim %s' % TOTALGAGALPOST).lcd_status()

#                     except TypeError as err:
#                         pass
#                     except ValueError as err:
#                         pass
#                     except IndexError as err:
#                         pass
#             else:
#                 pass
#                 cetak.printLCD('Tidak Ada','Absensi Baru').lcd_status()
#         else:
#             pass
#             cetak.printLCD('Mac Fingerprint','Tidak Terdaftar').lcd_status()
#             time.sleep(3)
#             cetak.printLCD('Hubungi Kominfo','Untuk Mendaftarkan').lcd_status()
#             time.sleep(3)

#     def kirimstatus(self):
#         cetak.printLCD('Mengirim Status','Data Raspberry').lcd_status()
#         tujuan  = self.tujuan
#         alamat  = self.alamat
#         mac     = Finger.ambilmacaddress(tujuan, alamat)
#         pegawaifinger = Finger.semuadatapegawai(tujuan, alamat)
        

#         ip                  = alamat.replace(':80','')
#         versi               = Localhost.ambilversion()
#         jumlahmac           = Localhost.cekjumlahmac()
#         jumlahpegawaifinger = 0
#         jumlahadminfinger   = 0
#         for pegawai in pegawaifinger:
#             if str(pegawai[4].text) == str(0):
#                 jumlahpegawaifinger+=1
#             elif str(pegawai[4].text) == str(14):
#                 jumlahadminfinger+=1
#         jumlahabsensifinger = len(Finger.ambildataabsensi(tujuan, alamat))
#         jumlahpegawailocal  = Localhost.cekjumlahpegawai(mac)
#         jumlahadminlocal    = Localhost.cekjumlahadmin(mac)
#         jumlahabsensilocal  = Localhost.cekjumlahabsensi(mac)
#         instansiid          = instansi_id.ID_INSTANSI

#         encryptText     = str(ip) + str(versi) + str(jumlahmac) + str(jumlahpegawaifinger) + str(jumlahadminfinger) + str(jumlahabsensifinger) + str(jumlahpegawailocal) + str(jumlahadminlocal) + str(jumlahabsensilocal) + str(instansiid)
#         encryption      = encrypt(encryptText)
#         headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}
#         payload = {
#                      'ip'                  : ip,
#                      'versi'               : versi,
#                      'jumlahmac'           : jumlahmac,
#                      'jumlahpegawaifinger' : jumlahpegawaifinger,
#                      'jumlahadminfinger'   : jumlahadminfinger,
#                      'jumlahabsensifinger' : jumlahabsensifinger,
#                      'jumlahpegawailocal'  : jumlahpegawailocal,
#                      'jumlahadminlocal'    : jumlahadminlocal,
#                      'jumlahabsensilocal'  : jumlahabsensilocal,
#                      'instansi_id'         : instansiid,
#                      'token'               : encryption
#                     }
#         if Server.POST('LOGRASPBERRY', headers, payload):
#             cetak.printLCD('Berhasil Mengirim','Status Raspberry').lcd_status()
#         else:
#             cetak.printLCD('Gagal Mengirim','Status Raspberry').lcd_status()

# clearlog(tujuan, '10.10.10.10:80', '00:17:61:11:72:24')
# manajemenuser('Finger A', '10.10.10.10:80')
# normalizepegawai('Finger A', '10.10.10.10:80','00:17:61:11:72:24')
# daftarmac()
# Proses(tujuan, alamat).manajemenadmin()
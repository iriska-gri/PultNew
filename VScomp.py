import getpass # Определить пользователя

class VScomp():

    def __init__(self):

        self.usering = getpass.getuser()
        self.inTable = 'a_all_data_106'

        if self.usering == 'systemsupport':
            self.set_connect = ("localhost", "root", "P@ssw0rd")
            self.myBD = "sroki_svod"
            self.myBDokved = "okved"
            self.spravSNTS = 'sprav_snts_svod'
            self.tablemsp = 'viruzka_msp'
            self.tablenp = 'viruzka_np'
        else:
            self.set_connect = ("10.252.44.38", "root", "P@ssw0rd")
            self.myBD = "Sroki_svod"
            self.myBDokved = "OKVED"
            self.spravSNTS = 'sprav_SNTS_svod'
            self.tablemsp = 'Viruzka_MSP'
            self.tablenp = 'Viruzka_NP'

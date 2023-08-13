import yaml
class UserProfile:
    name = ''
    
    # Cycling power
    REST = 0
    MAP = 0
    FTP = 0

    # Cycling cadence
    IDLE = 0
    LOW = 0
    MED = 0
    HIGH = 0
    SPRINT = 0

    # Heart Rate zones (lower limit)
    Z2 = 0
    Z3 = 0
    Z4 = 0
    Z5 = 0
    MAX = 0
    

    
    def __init__(self,file_path):

        with open(file_path,'r') as file:
            user_profile = yaml.safe_load(file)

        self.name = str(user_profile['name'])

        self.REST = int(user_profile['REST'])
        self.MAP = int(user_profile['MAP'])
        self.FTP = int(user_profile['FTP'])

        self.IDLE = int(user_profile['IDLE'])
        self.LOW = int(user_profile['LOW'])
        self.MED = int(user_profile['MED'])
        self.HIGH = int(user_profile['HIGH'])
        self.SPRINT = int(user_profile['SPRINT'])

        self.Z2 = int(user_profile['Z2'])
        self.Z3 = int(user_profile['Z3'])
        self.Z4 = int(user_profile['Z4'])
        self.Z5 = int(user_profile['Z5'])
        self.MAX = int(user_profile['MAX'])


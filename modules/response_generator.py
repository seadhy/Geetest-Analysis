import json
import random
import hashlib
from modules.encryptor import Encryptor


class ResponseGenerator:
    def __init__(self, risk_type: str, lot_number: str, pow_detail: dict, captcha_id: str, distance: int = 0, passtime: int = 0, gobang_solution: list = [], icon_crusher_solution: list = []):
        self.risk_type = risk_type
        
        self.lot_number = lot_number
        
        self.version = pow_detail['version']
        self.bits = pow_detail['bits']
        self.datetime = pow_detail['datetime']
        self.hashfunc = pow_detail['hashfunc']
        self.version = pow_detail['version']
        
        self.captcha_id = captcha_id
        self.distance = distance
        self.passtime = passtime
        
        self.gobang_solution = gobang_solution
        
        self.icon_crusher_solution = icon_crusher_solution
        
        self.device_id = ''
        self.static_num = .8876 * 340 / 300
        
        self.BAG1 = [[[2, 3], [19, 20]], [[19], [2], [21], [16]], [[9], [22], [1], [8]]]
        self.BAG2 = [[[16, 23]]]
    
    
    def __generate_pow_msg(self):
        message_list = [self.version, str(self.bits), self.hashfunc, self.datetime, self.captcha_id, self.lot_number, '', Encryptor.generate_aes_key()]
        return '|'.join(message_list)
    
    
    def __get_string_by_lot_number(self, bag, lot_number):
        result = ''
        
        for arr in bag:
            for element in arr:
                first_index_val = element[0]
                second_val = element[1] + 1 if len(element) > 1 else element[0] + 1
                res = lot_number[first_index_val:second_val]
                result += res
            result += '.'
        
        return result.rstrip('.')
    
    
    def __generate_dynamic_val(self):
        dynamic_val_names = self.__get_string_by_lot_number(self.BAG1, self.lot_number).split('.')
        dynamic_val_value = self.__get_string_by_lot_number(self.BAG2, self.lot_number)
        
        last_dynamic_val_name = dynamic_val_names[0]
        last_dynamic_val_value = {dynamic_val_names[1]: {dynamic_val_names[2]: dynamic_val_value}}
        
        return last_dynamic_val_name, last_dynamic_val_value


    def generate(self):
        pow_msg = self.__generate_pow_msg()
        pown_sign = hashlib.md5(pow_msg.encode()).hexdigest()      
        
        last_dynamic_val_name, last_dynamic_val_value = self.__generate_dynamic_val()
        
        data = {
          'device_id': self.device_id,
          'lot_number': self.lot_number,
          'pow_msg': pow_msg,
          'pow_sign': pown_sign,
          'geetest': 'captcha',
          'lang': 'zh',
          'ep': '123',
          'biht': '1426265548',
          'OhUE': 'n1AM',
          last_dynamic_val_name: last_dynamic_val_value,
          'em': {
               'ph': 0,     # checkPhantom
               'cp': 0,     # checkCallPhantom
               'ek': '11',  # checkErrorKeys
               'wd': 1,     # checkWebDriver
               'nt': 0,     # checkNightmare
               'si': 0,     # checkScriptFn
               'sc': 0      # checkSeleniumMarker
            }
        }
        
        match self.risk_type:
            case 'ai':
                pass
            case 'slide':
                user_response = self.distance / self.static_num + 2
                data = {'setLeft': self.distance, 'passtime': self.passtime, 'userresponse': user_response} | data
            case 'winlinze':
                data = {'passtime': self.passtime, 'userresponse': self.gobang_solution} | data
            case 'match':
                data = {'passtime': self.passtime, 'userresponse': self.icon_crusher_solution} | data
        
        return json.dumps(data, separators=(',', ':'))
    
import binascii
import json
import random
import numpy as np
from uuid import uuid4
from curl_cffi import requests
from modules.encryptor import Encryptor
from modules.slide import SlideSolver
from modules.gobang import GobangSolver
from modules.icon_crusher import IconCrusherSolver
from modules.response_generator import ResponseGenerator


class GeeTest:
    def __init__(self, captcha_id: str, proxy: str):
        self.captcha_id = captcha_id
        self.challenge = str(uuid4())
        
        self.client_type = 'web'
        self.risk_type = 'slide'
        self.classical_risk_type = 'slide'
        
        self.session = requests.Session(impersonate='chrome131', proxies={'http': 'http://' + proxy, 'https': 'http://' + proxy})
        
    def __get_task(self):
        callback = 'geetest_' + Encryptor.generate_ts()
        params = {
            'callback': callback,
            'captcha_id': self.captcha_id,
            'challenge': self.challenge,
            'client_type': self.client_type,
            'risk_type': self.classical_risk_type,
            'lang': 'en'
        }
        
        resp = self.session.get('https://gcaptcha4.geetest.com/load', params=params)
        
        if resp.status_code != 200:
            return False

        json_resp = Encryptor.read_geetest(callback, resp.text)
        
        if json_resp['status'] != 'success':
            return False
                
        return json_resp['data']
    
    def __load_for_second_time(self, lot_number: str, payload: str, process_token: str, payload_protocol: str):
        callback = 'geetest_' + Encryptor.generate_ts()
        
        params = {
            'callback': callback,
            'captcha_id': self.captcha_id,
            'client_type': self.client_type,
            'lot_number': lot_number,
            'risk_type': self.classical_risk_type,
            'pt': '1',
            'lang': 'en',
            'payload': payload,
            'process_token': process_token,
            'payload_protocol': payload_protocol,
        }
        
        resp = self.session.get('https://gcaptcha4.geetest.com/load', params=params)
        
        if resp.status_code != 200:
            return False
        
        json_resp = Encryptor.read_geetest(callback, resp.text)
        if json_resp['status'] != 'success':
            return False
    
        return json_resp['data']
    
    
    def __get_image_data(self, image_url: str):
        img_content = self.session.get(image_url).content
        
        return np.frombuffer(img_content, dtype=np.uint8)
    
    
    def __generate_w(self, response: str):
        aes_key = Encryptor.generate_aes_key()
        rsa_data = Encryptor.generate_rsa(aes_key)
                
        aes_data = Encryptor.aes_encrypt(response, aes_key)
        string_aes_data = binascii.hexlify(bytearray(aes_data)).decode()
                
        w = string_aes_data + rsa_data
        
        return w
        
    
    def __verify(self, lot_number: str, payload: str, process_token: str, payload_protocol: str, w: str):
        callback = 'geetest_' + Encryptor.generate_ts()
        
        params = {
            'callback': callback,
            'captcha_id': self.captcha_id,
            'client_type': self.client_type,
            'lot_number': lot_number,
            'risk_type': self.risk_type,
            'payload': payload,
            'process_token': process_token,
            'payload_protocol': payload_protocol,
            'pt': '1',
            'w': w,
        }
        
        resp = self.session.get('https://gcaptcha4.geetest.com/verify', params=params)
                        
        if resp.status_code != 200:
            return False
        
        json_resp = Encryptor.read_geetest(callback, resp.text)
        if json_resp['status'] != 'success':
            return False
                
        if json_resp['data']['result'] == 'continue':  # this part is not working fully but if you use quality proxy, probably u wont have to use this part
            # raise Exception()
            return 'CONTINUE'
        
        return json_resp['data']['seccode']
    
    
    def solve_for_ai_captcha(self, task):                
        lot_number = task['lot_number']
        payload = task['payload']
        process_token = task['process_token']
        payload_protocol = task['payload_protocol']
        
        pow_detail = task['pow_detail']
                
        response = ResponseGenerator(
            risk_type=self.risk_type,
            lot_number=lot_number,
            pow_detail=pow_detail,
            captcha_id=self.captcha_id,
        ).generate()
        
        w = self.__generate_w(response)
        
        response = self.__verify(lot_number, payload, process_token, payload_protocol, w)
        
        if response == 'CONTINUE': # can be flagged but its %99 proxy related
            task = self.__load_for_second_time(lot_number, payload, process_token, payload_protocol)
            if task['captcha_type'] == 'ai':
                self.solve_for_ai_captcha(task)
            
            
        response['risk_type'] = self.risk_type
        
        if response:
            return response
    
    
    def solve_for_slide_captcha(self, task):
        slide_img = 'https://static.geetest.com/' + task['slice']
        bg_img = 'https://static.geetest.com/' + task['bg']
        
        slide, bg = self.__get_image_data(slide_img), self.__get_image_data(bg_img)
        distance = SlideSolver(bg, slide).get_position()[0]  # x val of the solution
                        
        lot_number = task['lot_number']
        payload = task['payload']
        process_token = task['process_token']
        payload_protocol = task['payload_protocol']
        
        pow_detail = task['pow_detail']
                
        response = ResponseGenerator(
            risk_type=self.risk_type,
            lot_number=lot_number,
            pow_detail=pow_detail,
            captcha_id=self.captcha_id,
            distance=distance,
            passtime=random.randint(500, 700)
        ).generate()
        
        w = self.__generate_w(response)
        
        response = self.__verify(lot_number, payload, process_token, payload_protocol, w)
        response['risk_type'] = self.risk_type
        
        if response:
            return response
        
    def solve_for_gobang_captcha(self, task):
        ques = task['ques']
        solution = GobangSolver(ques=ques).found_last_piece()
        formatted_solution = [solution['piece'], solution['target']]
                
        lot_number = task['lot_number']
        payload = task['payload']
        process_token = task['process_token']
        payload_protocol = task['payload_protocol']
        
        pow_detail = task['pow_detail']
                
        response = ResponseGenerator(
            risk_type=self.risk_type,
            lot_number=lot_number,
            pow_detail=pow_detail,
            captcha_id=self.captcha_id,
            passtime=random.randint(500, 700),
            gobang_solution=formatted_solution
        ).generate()
        
        w = self.__generate_w(response)
        
        response = self.__verify(lot_number, payload, process_token, payload_protocol, w)
        response['risk_type'] = self.risk_type
        
        if response:
            return response
        
    def solve_for_icon_crusher_captcha(self, task):
        ques = task['ques']
        solution = IconCrusherSolver(ques=ques).find_icon_swap()
        formatted_solution = [solution['missing_icon'], solution['target_icon']]
                
        lot_number = task['lot_number']
        payload = task['payload']
        process_token = task['process_token']
        payload_protocol = task['payload_protocol']
        
        pow_detail = task['pow_detail']
                
        response = ResponseGenerator(
            risk_type=self.risk_type,
            lot_number=lot_number,
            pow_detail=pow_detail,
            captcha_id=self.captcha_id,
            passtime=random.randint(500, 700),
            icon_crusher_solution=formatted_solution
        ).generate()
        
        w = self.__generate_w(response)
        
        response = self.__verify(lot_number, payload, process_token, payload_protocol, w)
        response['risk_type'] = self.risk_type
        
        if response:
            return response
    
    def solve(self):
        task = self.__get_task()
        
        self.risk_type = task['captcha_type']
        
        if self.risk_type == 'ai':
            response = self.solve_for_ai_captcha(task)
        elif self.risk_type == 'slide':
            response = self.solve_for_slide_captcha(task)
        elif self.risk_type == 'winlinze':
            response = self.solve_for_gobang_captcha(task)
        elif self.risk_type == 'match':
            response = self.solve_for_icon_crusher_captcha(task)
        
        if response.get('pass_token'):
            response['status'] = 'solved'
        else:
            response['status'] = 'failed'
        
        return response

if __name__ == '__main__':
    PROXIES = open('assets/proxies.txt').read().splitlines()

    geetest_session = GeeTest(
        captcha_id='fcd636b4514bf7ac4143922550b3008b',
        proxy=random.choice(PROXIES)
    )
    
    solution = geetest_session.solve()
    print(json.dumps(solution, indent=4))
    

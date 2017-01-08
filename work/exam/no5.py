# -*- encoding:utf-8 -*-

import re
import base64
import json

security_key='wesdgwegt'


def get_users():
    try:
        with open('users') as f:
            dc=json.load(f)
            return dc
    except IOError as e:
        return {}

def chang_pswd(old_pswd):
    print('please input old pswd')
    input_pswd=raw_input()
    if input_pswd==old_pswd:
        return two_input_pswd()
    else:
        return chang_pswd(old_pswd)

def two_input_pswd():
    try:
        print('please first input pswd')
        first_pswd=raw_input()
        valide_pswd(first_pswd)
        print('please second input pswd')
        secod_pswd=raw_input()
        if first_pswd == secod_pswd:
            return first_pswd
        else:
            raise UserWarning,'first and seconde is diffrent'
    except UserWarning as e:
        print(e)
        return two_input_pswd()
    

def valide_pswd(pswd):
    a_capital=re.search('[A-Z]',pswd)
    if not a_capital:
        raise UserWarning,'password need a captical'
    a_lower=re.search('[a-z]',pswd)
    if not a_lower:
        raise UserWarning,'password need a lower letter'
    eight_long= (len(pswd)>=8)
    if not eight_long:
        raise UserWarning,'password need at leaset 8 long'


def jiami(pswd):
    pswd+=security_key
    return base64.b64encode(pswd)

def jiemi(pswd):
    pswd=base64.b64decode(pswd)
    pswd=pswd.rstrip(security_key)
    return pswd

if __name__=='__main__':
    users=get_users()
    print('enter your name')
    name=raw_input()
    old_pswd=users.get(name)
    if old_pswd:
        old_pswd=jiemi(old_pswd)       # 解密
        pswd=chang_pswd(old_pswd)
    else:
        pswd=two_input_pswd()
    users[name]=jiami(pswd)            # 加密
    
    with open('users','w') as f:
        json.dump(users,f)
        print('Password set successfully')
    
# -*- encoding:utf-8 -*-
import re

importent_domain=['google.com']

def validate_email(email):
    mt=re.match('(\w+)@(\w+)\.(\w+)', email)
    if mt:
        name=mt.group(1)
        domain=mt.group(2)+'.'+mt.group(3)
        advise_domain= check_importent_domain(domain)
        if advise_domain:
            choice =prompt_adviese(name, advise_domain)
            if choice=='y':
                return '%s@%s'%(name,advise_domain)
            else:
                return email            
    else:
        print('error email format')

def check_importent_domain(domain):
    if domain in importent_domain:
        return 
    else:
        return advise(domain)
       

def advise(domain):
    likely_domain=domain
    current_degree=0
    for item in importent_domain:
        degree=like_degree(domain,item)
        if degree>current_degree:
            current_degree=degree
            likely_domain=item
    return likely_domain

def like_degree(src,dst):
    """
    这里可以根据 模糊算法，计算匹配关系。。由于时间关系，统一返回 100
    """
    return 100

def prompt_adviese(name,advise_domain):
    print('Did you mean %s@%s [y/n]'%(name,advise_domain))
    choice=raw_input()
    return choice
    


if __name__=='__main__':
    print( validate_email('heyulin@smalltreemedia.com') )
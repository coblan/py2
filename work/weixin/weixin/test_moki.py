import requests
employee=[
    'olEWajneBxtIOchKQP9gukDJQdPg',
    'olEWajkpE4kzkOhfUg6PNTaFjMNg',
    'olEWajkwcff2p1osDhgwlZnSbmOE',
    'olEWajs9d2AdXvYB6K_fA7ldHkSY',
    'olEWajhyoRDJvoZ3hPAaXm_N2h0I',
    'olEWajqXS1WLdNP7zzBmh9aRahzE',
    'olEWajol7Guzu6hITLlkwwE6iJX0',
    'olEWajqCgBqjJ7VxI3YMUMpDGYAQ',
    'olEWajj_fMErlorJvn4roYr8Efh8',
    'olEWajoRzwnc2hnf7z_IBpk7nRVo',
    'olEWajiSzMCHUkqNue5zMg43gvKM',
    'olEWajlMsev72BCfqwuqlhJ1KCzg',
    'olEWajntzXstri74hNCnyv8oa1zc',
    'olEWajgQquMo58o3_ctX7guYYr-s',
    'olEWajp635hl1zWi7-EPIPZZbloA',
    'olEWajo0JVDjUHF9MENKoHQ2f9Mo',
    'olEWajhbjp5kTIsyIVqRdsytoaBg',
    'olEWajiRz5eNBAW2bVVHYUGx8o2w',
    'olEWajmwtcbnKxmlAiWZR_TO3wro',
    'olEWaju_n0WKxOPoF9tlTUq_pgNw',
    'olEWaji5vDvA68JUJHc29DqV2hNE',
    'olEWajsWqw2h2Ao7mWtRBtGCx6YQ',
    'olEWajgfgixvPm551jeD5N_yMtEw',
    'olEWajpkUDCOa-nSnpQWOPJacvLg',
    'olEWajvQL74VOco4VWI1ACB4nUt8',
    'olEWajpswDCXJ0b1u9YV2XCt0U1U',
    'olEWajgsNFspX2Hseq7z9RJdm7FQ',
    'olEWajlte3kGlBSm3khlt2K3m7bc',
    'olEWajuTsomOaB-_nJL3xN-Ki-l0',
    'olEWajs-ig-4n-zEIoqVKT9DQnPs',
    'olEWajnQ3jwNViRx8uwVvjvTlxT0',
    'olEWajj5yIWV0Llfw4fFTM3l6drY',
    'olEWajtzvsD0wl7sXt6TBEHsxFU8',
    'olEWajgghU7Vg6XiC4vo0LvGXqdM',
    'olEWajtKSr-xcWB6GL7iXU7fEhgM',
    'olEWajhZLfUJw7bF4mb0EqbrqlVc',
    'olEWajqcBb31X3mMBB_Jby75gN-M',
    'olEWajpwv_7simPccxW2sWDuU_nk',
    'olEWajpSOCqwAjCwToIQn5ibMlW4',
    'olEWajplzYFSg6b5azHu1qrgsRYA',
    'olEWajqv3mcNJaF6CW2TG2hWzHqM',
    'olEWajjfGAoDUgoisWAMXJVaTQRU',
    'olEWajgy_CtHt3LEyMeEu_q_XWrY',
    'olEWajkP5Czyea5dVaha4YzjJKYs',
    'olEWajqLJvlxvT_9pZtT5wYjI3_E',
    'olEWajqYJtITXSlahQ47NtEIdn7E',
    'olEWajtcPdAe93pSqhP4EOJTgXrs',
    'olEWajp-1qppFID7YZaA2KkdLTnc',
    'olEWajggFeaw_SUgD6GfReVSkbtE',
    'olEWajsCY_880S5n5s2bB1YVZRRI',
    'olEWajgyrcXMntB6b_VBxY9EwXc4',
    'olEWajiOlR7DOB9gM-ZBzZ9VMakM',
    'olEWajtDfKxeEhRUs0EJryE7CfCk',
    'olEWajil8h9_BhsqWs_gDgN3vsuU',
    'olEWajjSrB-nSNWjtWmZYeNC_3Ls',
    'olEWajkY0TbIMP5cQNbVPtTDLvT0',
    'olEWajrjY09HK-2C-7eQmkZ6mRhg',
    'olEWajsuP-QVZOB-mlITTb7huVus',
    'olEWajpLRhFphCMBjAGc_WDaTnso',
    'olEWajv9oEygptSl_-30leXwpfiM',
    'olEWajhzktNFuYqCz-1qnwRAkUNw',
    'olEWajuMR0ZbgcsGa7kH3gaSxuWk',
    'olEWajmjDTPN98rItVj_3zt5I-7s',
    'olEWajsZ9G604eJbkzUr6aDxgEHw',
    'olEWajt3t2mu_DN3o3cOecEivsX8',
    'olEWajmlPtntQNiUirx6APrg7HtY',
    'olEWajrLgqKlEawCgvCpNXLPw3gQ',
    'olEWajhZhliLs08YUR88zwsEBwKQ',
    'olEWajvT7xLWtJgQE_VYW1YCNBLQ',
    'olEWajk25OD7XjDBbbO356FBtChQ',
    'olEWajrxUOrb65aJf1yEU6ZtweYc',
    'olEWajj5AzxSjH0H3GZVeXlMEQYo',
    'olEWajqB00lEWpP_pimxev3M8FgQ',
    'olEWajuTBh8uZZ_A7Ml7LuX5LeCU',
    'olEWajt1ZSdifJ0VMRi1V8CEBfGw',
    'olEWajr8midgktavqRFxcRVTLlRU',
    'olEWajiY8vNZgFwQcNacknYQSTNs',
    'olEWajrW--C4PZf8QDPqt073loQg',
    'olEWajgzUXu33nwwdNCYUG1gneyY',
    'olEWajqBvdw-Z-QRzbrtwoYmqAGI',
    'olEWajj3x-7iA8vfCOCFp69L0Fh8',
    'olEWajpji6FqC5twaXFV7S929AnQ',
    'olEWajhq55m30-722l1W_dBcYCnA',
    'olEWajizj_Xgbtpx4SBJ2srqULRo',
    'olEWajhVZt-SSFD4M4Q8icEJOnkg',
    'olEWajuDIRLPOm9aqGVzZs40nAgU',
    'olEWajvjYnXLHBei4pQeJbqo-d5g',
    'olEWajkorI5KddNJfEGMbUd3najI',
    'olEWajpei0PV7QhcFbiWLdg5zYec',
    'olEWajl3ldgjvp3DQIjmbvyNOFMU',
    'olEWajne8HeFlvKnJUExbdsIVcqw',
    'olEWajqART-dNLbfqdOgAXkv4gZ0',
    'olEWajqUJ1NQAngLwlWA4Ai-57c4',
    'olEWajuhDr8Qz7Q3HG8Vn0Hi-26M',
    'olEWajmtyrYwtZtjvz3zQHUp4M2c',
    'olEWajjcyg2Fzak1zOwJ4fsq33LA',
    'olEWajhxvjhgcTqA_80ZCnmSIbXM',
    'olEWajgO90gg8giHMGfMEXwQIt4w',
    'olEWajjv-sx1dxtGZRtMYMPkrCHw',
    'olEWajstISiv2OavxtgPTgw2Sp8g',
    
    'olEWajrdQy2wIO2Hwz7t8oREG-RY',
    'olEWajnmtYvYWmV33ssT7kSNWB5s',
    'olEWajoj-A65ejjN0kUR6djvGEBs',
    'olEWajjoFgO11fmc5NMFe7pnIB6M',
    'olEWajpVAACfcWxsKLmSM8ismlks',
    'olEWajt5EedMsMtNpCdVLK-DlM9w',
    'olEWajuUY656x9-n_GZfop6id0tM',
    'olEWajsVxrlC2Qm1nl1vulsPybZk',
    'olEWajlUWx6ndunwo_Pby3aTT730',
    'olEWajrD6Ovuy3cUfIqU5R4hKMt8',
    'olEWajkpOcpAaBB4YxUmK70udxoA',
    'olEWajnoT5EulycWpZQ5KaEvY-1k',
    'olEWajhit9OQ1SkO2U6uU7igFzP4',
    'olEWajkRlSkKynfL53hVFAvxj4TU',
    'olEWajk11vVVX5V3TP2aB_cYrc4Q',
    'olEWajpmQ2OTE4N_zVvntdNRRmE0',
    'olEWajl7cZ5VJC3c3_7hXclmFA0E',
    'olEWajiUaQlwROPkNdCp1SX4leXM',
    'olEWajmciMhz0is0HsbKF3WiYY3I',
    'olEWajr2D2WGzIKq0qbZ4IGGUD4I',
    'olEWajkr0yodWBbB8CquR-hlVxYg',
    'olEWajiMh0Nqv_Gq1J1zZB100JWQ',
    'olEWajvHFFt4aS_D1l5OPTY1_Dmo',
    'olEWajvULAl1YPJSjXlYxPLopNFs',
    'olEWajtDXCvh2-pKSXAcXE4aJ_Zk',
    'olEWajul-HUhLS-cOtVp8zIU2Q0c',
    'olEWajm42qZYRSZ8o4bh3sqItmTs',
    'olEWajkdaRSqgAW4wqgJJslv4deM',
    'olEWajmAjk3ZjUGkVF1gbjZrU6PY',
    'olEWajuqKVu-eVFmOpShfv2klE8w',
    'olEWajre5k6ro1h-QO5umoLj4yyo',
    'olEWajg13-Im8hIIkzODHh21m_ps',
    'olEWajnLqaWyj7I9of89zg3e-yyA',
    'olEWajnPUzbpRRs352h2YG0Dblak',
    'olEWajh4mPtkYF9GglEBPR113dfA',
    'olEWajtSSIb2CtdAdpE5OwYSfxnI',
    'olEWajv3CmX-5tl-nFAZXgKGoLQA',
    'olEWajsgqlVsgK97QwTJRh3ni6Es',
    'olEWajqNaUBjljFNEMbOz1e7Oeqc',
    'olEWajpUzdEdm5kSpuadu0RNJGgM',
    'olEWajnPmpx8FLkxzRx7YnHwj-xA',
    'olEWajoz7ATVbDKpU95xeiluoHbQ',
    'olEWajtrPAUs06QMIOYhDWSiYR5s',
    'olEWajjutvnon5GkoYChLfW5cgDk',
    'olEWajuxWvkrv55psHjO9WLxLJE0',
    'olEWajhL8puDRumQEMPHXyK8vuIg',
    'olEWajnKUND62Nby2oB5HjgJttiQ',
    'olEWajrbbpYr0rhKr1sLUNt_M3jE',
    'olEWajka8t5QNMfz-ekDVMPjqjhk',
    'olEWajgU7KrJ_H30i4fZZDHCcld0',
    'olEWajvx-wryiIX6nkFPXGqHAUmw',
    'olEWajipa7x2HWB1E1HIkdft6PKI',
    'olEWajmhF09OCDq3GNHsvTTJBrsM',
    'olEWajgD0CU6uuYRtGfP8epQNYPQ',
    'olEWajoJS22e9wD52I2j_sLk9JUI',
    'olEWajqtoT0bzccKZut3vrcOh-38',
    'olEWajvUL992_eLfpKxPF6SXuqbk',
    'olEWajro7Z2uLDuVEBBAddH-ZQmg',
    'olEWajhItOShs3fGCToVprRxOGe4',
    'olEWajtY634416sVGM-rjjv8zU6s',
    'olEWajszeyTyAmWPOzS71OFBSxAk',
    'olEWajlUfQSv7YX_i4ZQNqRsqZTQ',
    'olEWajqsb2C8DFFuyUwmKjAARE_U',
    'olEWajmtxkvcJx_QYX_A74_sbcVo',
    'olEWajsO7z5dKyiA0QQ2pwk8MJBU',
    'olEWajo2aahIE5sCWDiS4Eq1I4oQ',
    'olEWajr2s6-yEULPyFvRMJeYLzc0',
    'olEWajrD3_yOa7ZkLOr-l1ezvsFQ',
    'olEWajsHu5djgTAAGw7R4Bzf8juI',
    'olEWajgu2nwdrbW50iZfgIB8vx_s',
    'olEWajjx22kcLcVgRNZLT2QJKxE8',
    'olEWajrYT5TbnzpHBK6B-hta1tXs',
    'olEWajh-wLucThdfEOQd3hlDwQLk',
    'olEWaji2jcGICKHngUwe7iuw1xZI',
    'olEWajhuUBA2wqhugF9-M9I7CU1s',
    'olEWajnqok14rnab4iUtKIxYuZKQ',
    'olEWaju3LZU-KmpVBXOGyBX82VSU',
    'olEWajlSLrByYLjr4FHwt8cVhPp4',
    'olEWajsJDM3T04ttmIEckB-su7hw',
    'olEWajkBmWlsMK9YRJAeQGdwpqeI',
    'olEWaju04vaKHr6r5aqKKq31RGK4',
    'olEWajriC9Ej2b_-ZpYoooZ-AOgo',
    'olEWajhAMM8z9yFYVvZrX9juOp98',
    'olEWajjJbb4y8iJnxj-XPlh3ph68',
    'olEWajkOD7IlheS2VQFbKkr5wwqI',
    'olEWaju54AriHFqhCa5Yweeqhueo',
    'olEWajhe-IXNPLtmfDeZCHjtDz5s',
    'olEWajko0rWfI4788gSHCjolAg4o',
    'olEWajm4Eh9ygmGn2dlGES-0zi1M',
    'olEWajjCv3z5Yw0MV9ltP2hujEC0',
    'olEWajgjqIMoGcyAkmH_EXuIElG8',
    'olEWajiIqvuAaw2XM97uItWsgZSc',
    'olEWajoNw0bDDNk5wBi8jmxtBmnc',
    'olEWajj-5Xde21axcLkwkiriM9FQ',
    'olEWajn4uDVKcrFKmHwCePf-3ZIg',
    'olEWajgjJDU2BkWiWiPGnHWHTyHA',
    'olEWajrJD8S1hz81kBoPhz9UWtik',
    'olEWajtK-YdZmw06ZfqD_xcTLOnk',
    'olEWajlucJnziG11Uhx89HcLJIlI',
    'olEWajmBSHenwsm6riZwnqcXyCmQ', 
    
    'olEWajkAobBzO1wpEHdi8rk_UWXE',
    'olEWajmv75wV_T67SwHRohmr9cqE',
    'olEWajilZEG2KHexqObhWsriHzzY',
    'olEWajmaW0S6N82aUC8J1EZtynTI',
    'olEWajgBFVo2QE3a9YcdO5Wv_WGw',    
]

def access_token():
    '''获取accses_token,
    '''
    mokiappid='wx4caa217911a92dbd'
    mokisecret='257666d2ee35c47df38f4f6dd759813e'
    appid = mokiappid
    secret=mokisecret
    #moki
    # appid = 'wx4caa217911a92dbd'
    # secret = '257666d2ee35c47df38f4f6dd759813e'
    rq = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appid+'&secret='+secret)
    print(rq.text) 


def send(token):
    url = r'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='+token
    #post数据格式
    data= """
    {
        "touser": "olEWajpji6FqC5twaXFV7S929AnQ", 
        "text": {
            "content": "点击我(https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx4caa217911a92dbd&redirect_uri=http%3a%2f%2fwechat.mokitech.com%2fnianhui%2fjiemu%2f&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect)"
        }, 
        "msgtype": "text"
    }
    """
    rq = requests.post(url,data)
    print(rq.text)

def mock_usertextMsg(openid,url,content):
    data ="""<xml><ToUserName><![CDATA[gh_7b76db9b0422]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>1446453151</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml>
        """%(openid,content)    
    headers = {'content-type': 'text/xml'}
    rq= requests.post(url, data=data, headers=headers)
    print(rq.text)   
    
def test_local():
    '测试本地服务器的post XML的功能'
    # data ="""<xml><ToUserName><![CDATA[gh_7b76db9b0422]]></ToUserName>
# <FromUserName><![CDATA[o6hHBv1AfKq8rH5LAY6AY_gHbQrc]]></FromUserName>
# <CreateTime>1446453151</CreateTime>
# <MsgType><![CDATA[event]]></MsgType>
# <Event><![CDATA[CLICK]]></Event>
# <EventKey><![CDATA[V1001_GOOD]]></EventKey>
# </xml>
    # """
    # moki某人:olEWajiSzMCHUkqNue5zMg43gvKM
    data ="""<xml><ToUserName><![CDATA[gh_7b76db9b0422]]></ToUserName>
<FromUserName><![CDATA[olEWajiSzMCHUkqNue5zMg43gvKM]]></FromUserName>
<CreateTime>1446453151</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[这里是内容]]></Content>
</xml>
    """    
    headers = {'content-type': 'text/xml'}
    local="http://127.0.0.1:8000/nianhui/weixin/"
    web = "http://wechat.mokitech.com/nianhui/weixin/"
    rq= requests.post(local, data=data, headers=headers)
    print(rq.text)

def test_qiangda():
    # url= "http://wechat.mokitech.com/nianhui/weixin/"
    url = 'http://127.0.0.1:8000/nianhui/weixin/'
    content='我来抢答'
    mock_usertextMsg('olEWajneBxtIOchKQP9gukDJQdPg', url, content)
    
def test_qiangda_many():
    url= "http://wechat.mokitech.com/nianhui/weixin/"
    # url = 'http://127.0.0.1:8000/nianhui/weixin/'
    content= '测试抢答'
    for openid in employee:
        mock_usertextMsg(openid, url, content)


if __name__ =='__main__':
    
    # access_token()
    # test_qiangda()
    # test_qiangda_many()
    send("t10ZdyaofDB3ocdwstLTyX-K85jCAAopaG0XKnioEd_031kSXlj7jqsYJTH2gPG-rvdOzEmcRNnTCyRhxwV4SEXPRTCMd_xUhwJ-QbdrvtEHNIjACAWCX")
    
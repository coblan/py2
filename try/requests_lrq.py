import requests
# url='https://play.google.com/store/apps/details?id=com.degoo.android.washpet'
# headers={
    # 'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    # 'cookie':'SID=DQAAAL0BAADokD48xClLkMXcPVQf--G3eQq5bHhFeSjczoyC2aLfbOplMURNFuNKLOY6poSyOZTJhpr4ljhArtyrEVLDEzNbOKWVhxc6HYW86kl4n5f7QvPLdrpNCrSIZ8O5QR-VQ5NKjwhy7BrtoFnAwrbcK3DMad8XstWf55b0K3L83-S7itqJm_5iVDpgsvF_phnjz5xW87nSvHOkCjWvMigF89U409o_xDd-T3-Tzm6k7eRDup3wdbvBWtS-Gwu_otpJ6yZUMeilyYvPMcHWnehT_ep2enDr1ou70x6Jjjnvb3Y3uNp1AOyaCa1DU8Mnu1rZXoKSL0xBWfjKmFn2LdL1FYzPMKolD7rSQO7vtcLL11G40INEKirbVNUizq5o3CGeJFcNnTA1oeqyG5bmodph044ZPaywvviEhjWL88bYmywBpmzFtzTKBdDQCZmZOHv6M2EPX2iy1-PzuFYKAMqZ3WKsgZ8FphQXoz5dOBaHxfEUdNpEKgUkzMRBs33CE0a_LvmbyOjggkpWuL5wjc8eK_E3QZ_8xgZzHMkHbRDKdscyaYzj4Eb6aG5U8irHe_EU3Kefwc3qKuIKbZyB4QjfqTcH; HSID=A66wfXAg6UQDXIh-I; SSID=A4NRqVTchltyIQ0L5; APISID=gPKSlWIh7ssZ532K/Aj8a_vca4ky1SrO0u; SAPISID=lsx_W3JU8HeD2euU/AZ63Jap8UcxFBunmv; NID=75=Y7TuFQWaZwDygqwO3bejXxliUNC2PTXeLCR5Bfg_Pwb5vQFWzCeRkOTPNSbDN2rV2UsI7H6VvasVv8Dmsm5DLYt3DXLWAUvPgsc888WEUl0xL_gizOHXI6VOqmGX4qJW5Z0ZlUgueXURrj10EFmj4fnsWZ9hixP3YhbgbK9CpORW8ROubwySMkLJJqHdOx9EjWqBZwFA4BKrrWwznxcJWukDqrXmITnshpTAxNmY_bCvph-l3iG-rw5o2lzWscDISV15Aw; PLAY_ACTIVE_ACCOUNT=ICrt_XL61NBE_S0rhk8RpG0k65e0XwQVdDlvB6kxiQ8=heyulin@smalltreemedia.com; PLAY_PREFS=CuIDCJPb0I_uHBLYAwoCSEsQ-ba_yKUqGp0DERITFBUWGNQB1QGnAtkDwgTEBOMF5QXoBdcG2AbeBt8GkJWBBpGVgQaSlYEGk5WBBpSVgQaXlYEGpJWBBq2VgQa4lYEGwZWBBsSVgQbFlYEGyJWBBs6VgQbPlYEG0JWBBtSVgQbZlYEG8pWBBviVgQaEloEGh5aBBoyWgQaOloEGkZaBBp2WgQaeloEGn5aBBqCWgQalloEGppaBBqeWgQaoloEGypeBBu6XgQbvl4EGhZiBBr6YgQajm4EGrZuBBsubgQa8nYEGw52BBsSdgQbFnYEGxp2BBsedgQbdnYEG7J2BBpCegQaWnoEGxJ-BBvufgQakoIEG9KCBBvWggQbuoYEG8aGBBuKigQbqooEG86KBBveigQaOo4EGr6OBBrGjgQaapIEG76SBBvOkgQavpYEG6qWBBv6lgQadpoEGxqaBBrengQbHp4EGxKiBBsuogQbNqIEGzqiBBrCpgQa8rIEG-6yBBqyvgQbWr4EG16-BBsmwgQbYsYEGorKBBqOygQaksoEGq7KBBqyygQa9soEGxrKBBu-zgQYo-ba_yKUqOiRiYTMyNDFmYi0xMjIxLTQ4MjQtYWM3YS04OTU4NWJkMjliNGM:S:ANO1ljKN5MIVI8_L-Q; _gat=1; _ga=GA1.3.1080697781.1451449401'
# }
# rt=requests.get(url,headers=headers)
# ss=rt.text
# with open('d:/ff.html','w') as f:
    # f.write(ss.encode('utf8'))

# url='http://api.uacar.cn/sms/validatecode/?mobile=1235&vcode=666'
url='http://localhost:8000/sms/validatecode/?mobile=1235&vcode=4444'
url ='http://localhost:8000/user/regist'
data={
    'test':'111'
}
data ='mobile=17138080650&vcode=4566&nosign=1'
data='car_no=%E4%BA%ACW34567&nick=%E8%8B%B1%E9%9B%84%E4%B8%8A%E5%BA%A7&car_brand=&car_model=&passwd=e10adc3949ba59abbe56e057f20f883e&nosign=1'

url = 'http://localhost:8000/user/updateuserhead'
data = 'uid=2&usersession=18&head=http%3A%2F%2Fwx.qlogo.cn%2Fmmopen%2FQ3auHgzwzM5ib2aEwMZu68rRlbWEr4j3FciaQyb8WTdX9PK4iaruybtzO8zc7xjTXnUueIp6rwka5opqPXibjYwOZg%2F0&nosign=1'

rt = requests.post(url,data)
print(rt.text)
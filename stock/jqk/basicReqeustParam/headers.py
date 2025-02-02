from stock.jqk.basicReqeustParam.userAgent import get_user_agent

cookie = 'u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0.0; u_dpass=Fqf6NazqZGlIB3lOrvjbqUs11PvP1zJyu2vjNJOvTKEW0P2YABli3mGMCoC8RJSYHi80LrSsTFH9a%2B6rtRvqGg%3D%3D; u_did=B4E5A3F87E20418FB9A9AF9BF02F26C4; u_ttype=WEB; user=MDp3b2xmd2VsbDo6Tm9uZTo1MDA6MTg0MTgwNjMyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI3Ojo6MTc0MTgwNjMyOjE3MzczMDIxMTE6OjoxMzc5ODE3MTIwOjYwNDgwMDowOjEzZDgwZGY4ZWEyNGQzZDQ4YmVkMGViOWE0NDA3N2NhNTpkZWZhdWx0XzQ6MA%3D%3D; userid=174180632; u_name=wolfwell; escapename=wolfwell; ticket=85536d9ab1aea21dfabd678989930e68; user_status=0; utk=ea783d0cf5b7983692a23c9b9db8076a; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1737802495; HMACCOUNT=F59619CE9C15B76F; Hm_lvt_22a3c65fd214b0d5fd3a923be29458c7=1737802495; spversion=20130314; cmsad_170_0=0; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1737802813; searchGuide=sg; historystock=688692%7C*%7C688691%7C*%7C688256; Hm_lpvt_22a3c65fd214b0d5fd3a923be29458c7=1737806959; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1737806959; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1737806959; v=Ay8Xpt_5lDLF_ZAO5A1Jezglvkg81IP2HSiH6kG8yx6lkEE2SaQTRi34FyNS'

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'cid=dcfb1e098041b72ca5bbe96dc81caa211732111077; searchGuide=sg; historystock=300661; spversion=20130314; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1737250250,1737253355; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1737253366; u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0.0; u_dpass=KHxDY1XRNRrPNNUNpLHfbiYgSRFe%2BzqmzUnvsYu1dlQ68Z1Ln1mLUT05K0vxIU%2F0Hi80LrSsTFH9a%2B6rtRvqGg%3D%3D; u_did=1D467866FD3B40ECACAE484DF704AC5F; u_ttype=WEB; ttype=WEB; userid=174180632; u_name=wolfwell; escapename=wolfwell; user_status=0; user=MDp3b2xmd2VsbDo6Tm9uZTo1MDA6MTg0MTgwNjMyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI3Ojo6MTc0MTgwNjMyOjE3MzcyOTkyMTI6OjoxMzc5ODE3MTIwOjYwNDgwMDowOjE3NThkY2NiNTY4MDE3ODY0NWNlOGI3Y2Q2MzZiYzkyYjpkZWZhdWx0XzQ6MA%3D%3D; ticket=2300d9d454ae7500c9b0ada5694c6952; utk=b4f4b8735f6ed8e2ae43a4085da99ae4; v=A1mLKxPqWkW0mQbR_EIVVTw1aE465kjJN8hxFnsI0Xv-w3eywzZdaMcqgbYI',
    'Host': 'q.10jqka.com.cn',
    'Referer': 'https://q.10jqka.com.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'hexin-v': 'A1mLKxPqWkW0mQbR_EIVVTw1aE465kjJN8hxFnsI0Xv-w3eywzZdaMcqgbYI',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
chromeCommonHeaders = {
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',

    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

chromeHeaders = {
    **chromeCommonHeaders,
    'Accept': 'text/html, */*; q=0.01',
    'Cookie': cookie,
    'Host': 'q.10jqka.com.cn',
    'Referer': 'https://q.10jqka.com.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': get_user_agent(),
    'X-Requested-With': 'XMLHttpRequest',
    'hexin-v': 'A9_ntq-JxAKA78Ae34Wv4Gz9bjhsRDKUTZo3xnEtf3nUwPEmeRTDNl1oxyKC',
}

holderHeader = {
    **chromeCommonHeaders,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cache-Control': 'max-age=0',
    'Cookie': cookie,
    'Host': 'stockpage.10jqka.com.cn',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': get_user_agent(),
}

# print(rf'chromeHeaders is {chromeHeaders}')

tempHeader = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0.0; u_dpass=Fqf6NazqZGlIB3lOrvjbqUs11PvP1zJyu2vjNJOvTKEW0P2YABli3mGMCoC8RJSYHi80LrSsTFH9a%2B6rtRvqGg%3D%3D; u_did=B4E5A3F87E20418FB9A9AF9BF02F26C4; u_ttype=WEB; user=MDp3b2xmd2VsbDo6Tm9uZTo1MDA6MTg0MTgwNjMyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI3Ojo6MTc0MTgwNjMyOjE3MzczMDIxMTE6OjoxMzc5ODE3MTIwOjYwNDgwMDowOjEzZDgwZGY4ZWEyNGQzZDQ4YmVkMGViOWE0NDA3N2NhNTpkZWZhdWx0XzQ6MA%3D%3D; userid=174180632; u_name=wolfwell; escapename=wolfwell; ticket=85536d9ab1aea21dfabd678989930e68; user_status=0; utk=ea783d0cf5b7983692a23c9b9db8076a; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1737802495; HMACCOUNT=F59619CE9C15B76F; spversion=20130314; reviewJump=nojump; searchGuide=sg; usersurvey=1; historystock=688692%7C*%7C688691%7C*%7C688256; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1737807991; v=AyEZSF2D4mT4nk6QKpV_7Vp_MOY-zpXAv0I51IP2HSiH6k8Yyx6lkE-SSaUQ',
    'Host': 'basic.10jqka.com.cn',
    'Referer': 'https://stockpage.10jqka.com.cn/',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-site',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': get_user_agent(),
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',

}

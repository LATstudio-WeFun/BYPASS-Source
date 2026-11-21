# Red Square Bypass / BY BYPASS.LAT
# Bypass directly without using any browser
import base64, hashlib, hmac as HM, json, os, random, re, sys, threading, time, uuid as uuidlib, urllib.parse as _up
from curl_cffi import requests as cr
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

KYS="https://kys.linkvertise.lol";UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
SENTRY="Sentry!!!!j`C}/UOF@G/c*m;K>z*nb8Yib$NxOW=";HSU="0dc5fe881b7e46642035b85eb829446a0dfd07720cb8d9be8bfd0787eb73b4463cec88e67aeb4fd9bd4b778f7e4d24153759e53998c24eda9b5c49f3e048f4d0"
IP=".".join(str(random.randint(1,254)) for _ in range(4));REF2=KYS+"/vm/Z/1?info=Link+Is+Sandboxed!!";T0=time.time()
def hm(k,m):return HM.new(k,m,hashlib.sha256).digest()
def hm512(k,m):return HM.new(k,m,hashlib.sha512).digest()
def b64d(s):return base64.b64decode(s+"="*(-len(s)%4))
def b64e(b):return base64.b64encode(b).decode()
def hkdf_raw(ikm,salt,info,n):
    prk=hm(salt if salt else b"\x00"*32,ikm);t,ok,c=b"",b"",1
    while len(ok)<n:t=hm(prk,t+info+bytes([c]));ok+=t;c+=1
    return ok[:n]
def uuidh(b):
    if isinstance(b,str):b=b.encode()
    h=bytearray(hashlib.sha256(b).digest());h[6]=(h[6]&15)|64;h[8]=(h[8]&63)|128
    u=h.hex();return u[:8]+"-"+u[8:12]+"-"+u[12:16]+"-"+u[16:20]+"-"+u[20:32]+"-"+u[32:]
def ts():return "[%6.2f]"%(time.time()-T0)
def hdrs(bind):
    return {"x-RG-AntiCloudflareCH":bind,"x-RG-HostingSwitchUID":HSU,"x-RG-MosquitosBothers":uuidh(str(uuidlib.uuid4())),
            "sec-fetch-dest":"empty","sec-fetch-mode":"cors","sec-fetch-site":"same-origin",
            "sec-ch-ua":'"Not?A_Brand";v="24", "Chromium";v="152"',"sec-ch-ua-mobile":"?0","sec-ch-ua-platform":'"Windows"',
            "accept-language":"en-US,en;q=0.9","priority":"u=1, i"}

class Tunnel:
    def __init__(self,ky,ref):
        r0=ky.get(KYS+"/api/rg/encrypt-tunnel/PGPG",params={"RG_Ant":uuidh(str(uuidlib.uuid4()))},impersonate="chrome",timeout=15,headers={"Referer":ref})
        pg=r0.json();P,ws=pg["Payload"],pg["W_Sign"];ts=P["SrvEpoch"]//10000
        priv=X25519PrivateKey.generate()
        p1=priv.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw).hex()
        sh1=priv.exchange(X25519PublicKey.from_public_bytes(bytes.fromhex(P["P1"])))
        tsObj=json.dumps({"ch":{"x25519":p1,"cipher":P["YX_CIPHER"],"ts":ts},"sh":{"x25519":P["P1"],"sig":ws,"epoch":P["SrvEpoch"]},"params":{"protocol":SENTRY,"cipher":P["YX_CIPHER"]}},separators=(",",":"))
        salt=hashlib.sha256(tsObj.encode()).digest()
        self.okm=hkdf_raw(sh1,salt,SENTRY.encode(),256);self.bind=P["BIND"]
        self.cks=hkdf_raw(self.okm[:32],b"\x00"*32,b"YX-CK-SEND",32)
        self.ckr=hkdf_raw(self.okm[:32],b"\x00"*32,b"YX-CK-RECV",32);self.seq=0
        iv=os.urandom(12)
        enc=iv+AESGCM(self.okm[:32]).encrypt(iv,json.dumps({"SecureChannelEstablished":True,"KeyID":self.bind},separators=(",",":")).encode(),None)
        r2=ky.post(KYS+"/api/rg/encrypt-tunnel/PGPSC",params={"token":p1,"hmacv":self.bind},data=json.dumps({"encrypted":b64e(enc),"troubleshooter":uuidh(self.okm.hex()+p1+self.bind),"yx_cipher":"AES-256-GCM"},separators=(",",":")),impersonate="chrome",timeout=15,headers={"Content-Type":"application/json","Origin":KYS,"Referer":ref})
        self.ok=r2.status_code==200
    def smk(self):
        mk=hkdf_raw(self.cks,b"\x00"*32,b"YX-MSG",32);self.cks=hkdf_raw(self.cks,b"\x01"*32,b"YX-CK-ADV",32);sq=self.seq;self.seq+=1;return mk,sq
    def rmk(self,seq):
        ck,mk=self.ckr,None
        for _ in range(seq+1):mk=hkdf_raw(ck,b"\x00"*32,b"YX-MSG",32);ck=hkdf_raw(ck,b"\x01"*32,b"YX-CK-ADV",32)
        return mk
    def ge(self,mk,o):
        pt=o if isinstance(o,bytes) else json.dumps(o,separators=(",",":")).encode()
        iv=os.urandom(12);return b64e(iv+AESGCM(mk).encrypt(iv,pt,None))
    def gd(self,mk,b64):
        raw=b64d(b64);return AESGCM(mk).decrypt(raw[:12],raw[12:],None)
    def hd2(self):
        return hdrs(self.bind)
    def env(self,mk,obj,sq):
        x1=self.ge(mk,obj)
        s2={"fingerprint":HSU,"KeyID":self.bind,"Machine__IPV4":IP,"PL1_RMethod":"POST","B_UserAgent":UA,"RG_FpFlags":0,"RG_WkB":False,"R_Timestamp":int(time.time()*1000),"PL1_HashedC":uuidh(x1),"yx_seq":sq}
        x2=self.ge(mk,s2)
        return {"payload":x1,"uuid":uuidh(x1),"anti-tamper":True,"payload2":x2,"fingerprint":uuidh(x2),"hmac":b64e(hm512(mk,x1.encode())),"seq":sq}
    def eget(self,rj):
        mk=self.rmk(rj.get("seq",0));return self.gd(mk,rj["payload"]).decode("utf-8","replace")
    def epost(self,ky,path,obj,ref):
        mk,sq=self.smk()
        r=ky.post(KYS+path,data=json.dumps(self.env(mk,obj,sq),separators=(",",":")),impersonate="chrome",timeout=15,headers={**self.hd2(),"Content-Type":"application/json","Origin":KYS,"Referer":ref})
        out={"s":r.status_code}
        try:
            rj=r.json()
            if r.status_code==200 and "payload" in rj:
                mk2=self.rmk(rj.get("seq",0));out["d"]=self.gd(mk2,rj["payload"]).decode("utf-8","replace")
            else:out["b"]=r.text[:200]
        except Exception as e:out["e"]=str(e)[:60]
        return out

def verify_single(ky,tc,lv):
    tcq=_up.parse_qs(_up.urlparse(tc).query)
    uid=tcq.get("uuid",[""])[0];tp=tcq.get("TaskID",[""])[0]
    tb=tc.split("#")[0];ref=_up.quote(tb,safe=":/?&=")
    try:ky.get(tc,impersonate="chrome",timeout=20,headers={"Referer":lv} if lv else {})
    except:pass
    print(ts(),"tc page uid="+uid[:8]+" task="+tp[:8])
    TB=Tunnel(ky,ref)
    if not TB.ok:raise RuntimeError("Red Square Link: secure tunnel rejected")
    fi=ky.get(KYS+"/api/v2/backWallZ/ForwardInfo_E2EE",params={"goy_id":tp},impersonate="chrome",timeout=15,headers={**TB.hd2(),"Referer":ref})
    try:print(ts(),"forwardinfo %s"%TB.eget(fi.json())[:60])
    except:print(ts(),"forwardinfo dec-fail")
    st={"hs":None,"lock":threading.Lock()}
    def b1s():
        try:
            s5=cr.Session();s5.headers.update({"User-Agent":UA});s5.cookies.update(ky.cookies)
            rr=s5.get(KYS+"/api/RTDL/v4/SquareVM",params={"RG_Socks":str(uuidlib.uuid4())},impersonate="chrome",timeout=(10,45),stream=True,headers=TB.hd2())
            buf={}
            for ln in rr.iter_lines():
                if ln is None:continue
                x=ln.decode("utf-8",errors="replace") if isinstance(ln,bytes) else ln
                if x=="":
                    if buf:
                        try:fx=json.loads(buf.pop("data",""))
                        except:fx={}
                        if fx.get("content"):
                            raw=b64d(fx["content"])
                            try:fx["_dec"]=AESGCM(TB.okm[:32]).decrypt(raw[:12],raw[12:],None).decode()
                            except:fx["_dec"]=""
                            with st["lock"]:
                                if st["hs"] is None:
                                    try:st["hs"]=json.loads(fx["_dec"])
                                    except:pass
                        buf={}
                    continue
                if x.startswith("data:"):buf["data"]=x[5:].lstrip()
        except:pass
    threading.Thread(target=b1s,daemon=True).start()
    te2=time.time()+8
    while time.time()<te2 and not st["hs"]:time.sleep(0.05)
    if st["hs"] and st["hs"].get("upload_endpoint"):
        uep=st["hs"]["upload_endpoint"]
        p1=TB.epost(ky,uep,{"type":"c_VMReady","payload":True},ref)
        p2=TB.epost(ky,uep,{"type":"c_IsVMVisible","payload":{"visible":True,"hidden":False}},ref)
        p3=TB.epost(ky,uep,{"type":"EnigmaRTDL_Query","keepalive":True,"time":int(time.time()*1000)},ref)
        print(ts(),"rtdl %s %s %s"%(p1.get("s"),p2.get("s"),p3.get("s")))
    else:
        print(ts(),"rtdl no-handshake")
    rm=ky.get(KYS+"/api/v2/backWallZ/requestMoonbrick",params={"tid":tp,"uia":uid},impersonate="chrome",timeout=15,headers={**TB.hd2(),"Referer":KYS+"/taskCompleted"})
    try:md=json.loads(TB.eget(rm.json()));print(ts(),"moonbrick captcha=%s vpn=%s"%(md.get("CaptchaRequired"),md.get("blockforVPN")))
    except:print(ts(),"moonbrick parse-fail")
    sh=TB.epost(ky,"/api/v2/shouldShowOwnAdChallengeZ",{"UserID":uid,"TaskID":tp},ref)
    print(ts(),"shouldShow %s"%(sh.get("d") or sh.get("b") or "")[:80])
    cbb={"UserID":uid,"X000":False,"TaskID":tp,"PageReferer":lv,"PageURL":tb,"X001":1,"X002":True,"X003":[]}
    cb=TB.epost(ky,"/api/backend/checkForBypass.json",cbb,ref)
    cbd=cb.get("d","")
    print(ts(),"checkForBypass %s"%cbd[:200])
    dest="";used=""
    try:
        cd=json.loads(cbd);tr=cd.get("Tests_Result") or {}
        used=str(tr.get("used") or "")
        dv=tr.get("Destination")
        if isinstance(dv,dict):dv=dv.get("URL","")
        dest=dv or ""
    except:pass
    print("[%6.2f] total %.2fs"%(time.time()-T0,time.time()-T0))
    if not dest:
        msg=(used or cbd)[:130]
        pre="Red Square Link expired" if ("expire" in msg.lower() or "start over" in msg.lower()) else "Red Square Link rejected"
        raise RuntimeError(pre+": "+msg)
    return dest

class DetectionError(Exception):
    pass

def run(dtom):
    global KYS,REF2
    ky=cr.Session();ky.headers.update({"User-Agent":UA})
    hh=(_up.urlparse(dtom).hostname or "").lower()
    if hh in ("kys.linkvertise.lol","rs.linkvertise.lol","red-square.space"):
        KYS="https://"+hh;REF2=KYS+"/vm/Z/1?info=Link+Is+Sandboxed!!"
    if "/taskCompleted" in _up.urlparse(dtom).path:
        print(ts(),"direct taskCompleted input")
        return verify_single(ky,dtom,"")
    dtom=dtom.split("?")[0].split("#")[0]
    tid=dtom.rsplit("/",1)[1]
    kd=ky.get(dtom,impersonate="chrome",timeout=20)
    print(ts(),"dtom",kd.status_code,"taskid="+tid[:8])
    m=re.search(r'\{\\"prefix\\":.*?\}',kd.text) or re.search(r'\{"prefix".*?\}',kd.text)
    if m:
        spec=json.loads(m.group().replace('\\"','"'));bits=round(float(spec["diff"])*4);width=(bits+3)//4;spare=width*4-bits
        tp=time.time();nonce=0;pre=(spec["prefix"]+":").encode()
        while nonce<8000000:
            hh=hashlib.sha256(pre+str(nonce).encode()).hexdigest()
            v=int(hh[:width],16)
            if spare:v>>=spare
            if v==0:break
            nonce+=1
        tp=time.time()-tp;hr=nonce/tp/1000 if tp>0 else 0
        print(ts(),"pow diff=%s bits=%d nonce=%d %.1f kH/s hash=%s"%(spec["diff"],bits,nonce,hr,hashlib.sha256(pre+str(nonce).encode()).hexdigest()[:20]))
        mcsrf=re.search(r'name="rg_csrf"\s+value="([^"]+)"',kd.text)
        stc="";lvu=""
        try:
            rp=ky.post(dtom,impersonate="chrome",timeout=15,data={"rg_pow_prefix":spec["prefix"],"rg_pow_exp":str(spec["exp"]),"rg_pow_diff":str(spec["diff"]),"rg_pow_sig":spec["sig"],"rg_pow_nonce":str(nonce),"rg_csrf":mcsrf.group(1)},headers={"Referer":dtom,"Content-Type":"application/x-www-form-urlencoded"})
            print(ts(),"pow submit",rp.status_code)
            if rp.url and (_up.urlparse(rp.url).hostname or "") not in ("kys.linkvertise.lol","rs.linkvertise.lol","red-square.space"):
                lvu=rp.url
                q=_up.parse_qs(_up.urlparse(rp.url).query)
                if "redirect" in q:stc=_up.unquote(_up.unquote(q["redirect"][0]))
                else:return rp.url
        except:pass
        if stc:
            print(ts(),"linkvertise-target link")
            return verify_single(ky,stc,lvu)
    st={"TA":None,"hs":None,"frames":[],"lock":threading.Lock(),"s1":None,"err":None}
    ev=threading.Event()
    def b1():
        try:
            s1=cr.Session();s1.headers.update({"User-Agent":UA});s1.cookies.update(ky.cookies);st["s1"]=s1
            TA=Tunnel(s1,REF2)
            if not TA.ok:st["err"]="tunnelA rejected";ev.set();return
            st["TA"]=TA;print(ts(),"tunnelA ok bind="+TA.bind[:16])
            rr=s1.get(KYS+"/api/RTDL/v4/SquareVM",params={"RG_Socks":str(uuidlib.uuid4())},impersonate="chrome",timeout=(10,120),stream=True,headers=hdrs(TA.bind))
            def b1x():
                try:
                    sx=cr.Session();sx.headers.update({"User-Agent":UA});sx.cookies.update(s1.cookies)
                    sx.get(KYS+"/api/v1/securityFileID?v="+str(uuidlib.uuid4()),impersonate="chrome",timeout=8,headers={"Referer":REF2})
                    sx.post(dtom+"/adblock",data=json.dumps({"d":0}),impersonate="chrome",timeout=8,headers={"Referer":dtom,"Content-Type":"application/json"})
                except:pass
            threading.Thread(target=b1x,daemon=True).start()
            buf={}
            for ln in rr.iter_lines():
                if ln is None:continue
                t=ln.decode("utf-8",errors="replace") if isinstance(ln,bytes) else ln
                if t=="":
                    if buf:
                        try:fx=json.loads(buf.pop("data",""))
                        except:fx={}
                        if fx.get("content"):
                            try:fx["_dec"]=AESGCM(TA.okm[:32]).decrypt(b64d(fx["content"])[:12],b64d(fx["content"])[12:],None).decode()
                            except:fx["_dec"]=""
                        with st["lock"]:st["frames"].append(fx)
                        if st["hs"] is None:
                            try:st["hs"]=json.loads(fx["_dec"])
                            except:pass
                            print(ts(),"sse up ep=%s"%(st["hs"].get("upload_endpoint","") if st["hs"] else "?"))
                            ev.set()
                        buf={}
                    continue
                if t.startswith("data:"):buf["data"]=t[5:].lstrip()
        except Exception as e:
            st["err"]=str(e)[:80];ev.set()
    threading.Thread(target=b1,daemon=True).start()
    s=""
    dest2=""
    kys_hosts=("kys.linkvertise.lol","rs.linkvertise.lol","red-square.space")
    def is_kys(u):
        try:
            return (_up.urlparse(u).hostname or "") in kys_hosts
        except:
            return True
    for attempt in range(3):
        r=ky.get(KYS+"/TaskStarted/"+tid,params={"CA":str(uuidlib.uuid4())},impersonate="chrome",timeout=20,allow_redirects=False)
        print(ts(),"TS a%d: %s loc=%s"%(attempt,r.status_code,(r.headers.get("Location") or "")[:70]))
        for _ in range(10):
            loc=r.headers.get("Location","")
            if r.url and not is_kys(r.url):dest2=r.url;break
            if "s=" in loc:s=loc.split("s=")[-1].split("&")[0];break
            if not loc or r.status_code!=302:
                print(ts(),"TS stop: %s url=%s"%(r.status_code,(r.url or "")[:70]));break
            if loc.startswith("http") and not is_kys(loc):dest2=loc;break
            r=ky.get(loc if loc.startswith("http") else KYS+loc,impersonate="chrome",timeout=20,allow_redirects=False)
        if s or dest2:break
        time.sleep(0.5)
    if dest2:
        q2=_up.parse_qs(_up.urlparse(dest2).query)
        if "redirect" in q2:
            print(ts(),"linkvertise-target link (TaskStarted)")
            return verify_single(ky,_up.unquote(_up.unquote(q2["redirect"][0])),dest2)
        return dest2
    ky.get(KYS+"/vm/Z?v=5&s="+s,impersonate="chrome",timeout=10)
    rq=ky.get(KYS+"/vm/q",params={"s":s},impersonate="chrome",timeout=20,headers={"Referer":KYS+"/vm/Z?v=5&s="+s})
    vmq=rq.text.strip();parts=dict((mm.group(1),mm.group(2)) for mm in re.finditer(r"([A-Za-z]+)=([^&\s]*)",vmq))
    UID,TIDP=_up.unquote(parts.get("UserID","")),_up.unquote(parts.get("TaskID",""))
    DATA=_up.unquote(parts.get("data",""));IFRAME=_up.unquote(parts.get("iframeUrl",""))
    print(ts(),"vm/q uid=%s task=%s sid=%s"%(UID[:13],TIDP[:13],s[:10]))
    kfull=KYS+"/vm/Z"+(vmq if vmq.startswith("?") else "?"+vmq)
    ev.wait(10)
    if not st["TA"]:raise RuntimeError(st["err"] or "tunnelA timeout")
    if not st["hs"]:raise RuntimeError("no sse first frame (link likely used)")
    try:ky.cookies.update(st["s1"].cookies)
    except:pass
    TA=st["TA"]
    tb={"TB":None,"err":None,"th":None,"s3":None}
    def b2():
        try:
            s3=cr.Session();s3.headers.update({"User-Agent":UA});s3.cookies.update(ky.cookies);tb["s3"]=s3
            TB=Tunnel(s3,KYS+"/taskCompleted?session="+UID+"&TaskID="+TIDP)
            if not TB.ok:tb["err"]="tunnelB rejected";return
            tb["TB"]=TB;print(ts(),"tunnelB ok bind="+TB.bind[:16])
        except Exception as e:tb["err"]=str(e)[:80]
    tb["th"]=threading.Thread(target=b2,daemon=True);tb["th"].start()
    def push(obj):
        mk,sqv=TA.smk();x1=TA.ge(mk,obj)
        s2={"fingerprint":HSU,"KeyID":TA.bind,"Machine__IPV4":IP,"PL1_RMethod":"POST","B_UserAgent":UA,"RG_FpFlags":0,"RG_WkB":False,"R_Timestamp":int(time.time()*1000),"PL1_HashedC":uuidh(x1),"yx_seq":sqv}
        x2=TA.ge(mk,s2)
        env={"payload":x1,"uuid":uuidh(x1),"anti-tamper":True,"payload2":x2,"fingerprint":uuidh(x2),"hmac":b64e(hm512(mk,x1.encode())),"seq":sqv}
        return ky.post(KYS+st["hs"]["upload_endpoint"],data=json.dumps(env,separators=(",",":")),impersonate="chrome",timeout=10,headers={**hdrs(TA.bind),"Content-Type":"application/json","Origin":KYS,"Referer":REF2}).status_code
    push({"type":"c_RequestVMConfig","payload":{"UserID":UID,"TaskID":TIDP,"V001":DATA,"V002":IFRAME}})
    te=time.time()+4;sv001=""
    while time.time()<te:
        with st["lock"]:
            for f in st["frames"]:
                try:
                    d=json.loads(f.get("_dec","{}"))
                    if d.get("type")=="s_VMConfig":sv001=d["payload"]["s_V001"]
                except:pass
            if sv001:break
        time.sleep(0.05)
    if not sv001:raise RuntimeError("no s_VMConfig")
    print(ts(),"vmcfg s_V001 ok")
    LOOT=""
    try:
        lg=ky.get(sv001,impersonate="chrome",timeout=6,allow_redirects=False,headers={"Referer":kfull})
        if lg.status_code in (301,302,303,307,308):LOOT=lg.headers.get("location","")
    except:pass
    print(ts(),"vguard mount %s"%(("302 loot=%dB"%(len(LOOT))) if LOOT else "no-redirect"))
    p1=push({"type":"c_VMReady","payload":True})
    p2=push({"type":"c_IsVMVisible","payload":{"visible":True,"hidden":False}})
    print(ts(),"vmready %d visible %d"%(p1,p2))
    tc=KYS+"/taskCompleted?session="+UID+"&TaskID="+TIDP
    tcr=ky.get(tc,impersonate="chrome",timeout=10,headers={"Referer":kfull})
    print(ts(),"taskCompleted",tcr.status_code)
    tb["th"].join(6)
    TB=tb["TB"]
    if not TB:raise RuntimeError(tb["err"] or "tunnelB timeout")
    try:ky.cookies.update(tb["s3"].cookies)
    except:pass
    fi_res=[]
    def bfi():
        try:
            s4=cr.Session();s4.headers.update({"User-Agent":UA});s4.cookies.update(ky.cookies)
            fi1=s4.get(KYS+"/api/v2/backWallZ/ForwardInfo_E2EE",params={"goy_id":TIDP},impersonate="chrome",timeout=15,headers={**TB.hd2(),"Referer":tc})
            fi_res.append(fi1.json())
        except:fi_res.append(None)
    tfi=threading.Thread(target=bfi,daemon=True);tfi.start()
    rm=ky.get(KYS+"/api/v2/backWallZ/requestMoonbrick",params={"tid":TIDP,"uia":UID},impersonate="chrome",timeout=15,headers={**TB.hd2(),"Referer":KYS+"/taskCompleted"})
    tfi.join(10)
    try:
        md=json.loads(TB.eget(rm.json()))
        print(ts(),"moonbrick captcha=%s vpn=%s incognito=%s"%(md.get("CaptchaRequired"),md.get("blockforVPN"),md.get("blockIncognito")))
    except:print(ts(),"moonbrick parse-fail")
    try:fi1d=TB.eget(fi_res[0]) if fi_res and fi_res[0] else ""
    except:fi1d=""
    print(ts(),"forwardinfo %s"%fi1d[:60])
    sh=TB.epost(ky,"/api/v2/shouldShowOwnAdChallengeZ",{"UserID":UID,"TaskID":TIDP},tc)
    print(ts(),"shouldShow %s"%sh.get("d",sh.get("b",""))[:90])
    cbb={"UserID":UID,"X000":False,"TaskID":TIDP,"PageReferer":LOOT,"PageURL":tc,"X001":1,"X002":True,"X003":[]}
    cb=TB.epost(ky,"/api/backend/checkForBypass.json",cbb,tc)
    cbd=cb.get("d","")
    print(ts(),"checkForBypass %s"%cbd[:200])
    dest="";det=False;used=""
    try:
        cd=json.loads(cbd)
        pbu=cd.get("postback_url","")
        if pbu:
            def _pb(u=pbu):
                try:
                    ss=cr.Session();ss.headers.update({"User-Agent":UA});ss.cookies.update(ky.cookies)
                    ss.get(u,impersonate="chrome",timeout=8)
                except:pass
            threading.Thread(target=_pb,daemon=True).start()
        tr=cd.get("Tests_Result") or {}
        det=bool(tr.get("detected"));used=str(tr.get("used") or "")
        dv=tr.get("Destination")
        if isinstance(dv,dict):dv=dv.get("URL","")
        dest=dv or ""
    except:pass
    print("[%6.2f] total %.2fs"%(time.time()-T0,time.time()-T0))
    if not dest:
        if det:
            raise DetectionError(used or cbd[:160])
        print(ts()+"err: no destination in checkForBypass: "+cbd[:180])
    return dest if dest.startswith("http") else None



if __name__=="__main__":
    try:r=run(sys.argv[1])
    except Exception as e:print("err: %s"%str(e)[:200]);r=None
    if r:print(r)
    sys.stdout.flush()
    os._exit(0)
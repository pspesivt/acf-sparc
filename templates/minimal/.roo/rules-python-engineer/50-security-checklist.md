Authentication&Authorization:
from passlib.context import CryptContext;pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_password(p):return pwd.hash(p)
def verify_password(p,h):return pwd.verify(p,h)
from jose import jwt;from datetime import datetime,UTC,timedelta
def create_access_token(user_id)->str:
    exp=datetime.now(UTC)+timedelta(minutes=15)
    c={"sub":str(user_id),"exp":exp,"iat":datetime.now(UTC),"type":"access"}
    return jwt.encode(c,settings.secret_key,algorithm="HS256")

InputValidation:
from sqlalchemy import select
stmt=select(User).where(User.email==email);result=await session.execute(stmt)
from pydantic import BaseModel,EmailStr,Field,field_validator
class UserInput(BaseModel):
    email:EmailStr
    username:str=Field(...,min_length=3,max_length=50,pattern="^[a-zA-Z0-9_-]+$")
    age:int=Field(...,ge=13,le=120)
    @field_validator("username",classmethod)
    def v(cls,v:str)->str:
        dangerous=["<script","javascript:","onerror=","onclick="]
        if any(d in v.lower() for d in dangerous):raise ValueError
        return v

XSS:
import html;return f"<h1>Welcome {html.escape(user_input)}</h1>"
from jinja2 import Environment,select_autoescape
env=Environment(autoescape=select_autoescape(["html","xml"]))
import json;response=json.dumps({"user":username})

CSRF:
from secrets import token_urlsafe,compare_digest
class CSRF:gen=lambda:token_urlsafe(32);validate=lambda s,r:compare_digest(s,r)
@app.middleware("http")
async def m(request,call_next):
    if request.method in ["POST","PUT","DELETE","PATCH"]:
        st=request.session.get("csrf_token");rt=request.headers.get("X-CSRF-Token")
        if not st or not rt or not compare_digest(st,rt):
            return JSONResponse(status_code=403,content={"detail":"CSRF invalid"})
    return await call_next(request)

SecretManagement:
from pydantic_settings import BaseSettings,field_validator
class Settings(BaseSettings):
    secret_key:str;database_url:str;api_key:str
    @field_validator("secret_key",classmethod)
    def vs(cls,v:str)->str:
        if len(v)<32:raise ValueError
        return v

FileUploadSecurity:
import hashlib,mimetypes;from pathlib import Path
ALLOWED={".jpg",".jpeg",".png",".pdf"};MAX=10*1024*1024
async def secure_file_upload(file,user_id)->Path:
    c=await file.read();assert len(c)<=MAX
    e=Path(file.filename).suffix.lower();assert e in ALLOWED
    m=mimetypes.guess_type(file.filename)[0];assert m in ["image/jpeg","image/png","application/pdf"]
    h=hashlib.sha256(c).hexdigest();n=f"{user_id}_{h}{e}"
    p=Path("/var/uploads")/n;p.write_bytes(c);return p

RateLimiting:
from datetime import datetime;import redis.asyncio as redis
class RateLimiter:
    def __init__(self,r):self.r=r
    async def is_allowed(self,key,max_requests,window_seconds):
        now=datetime.now().timestamp();ws=now-window_seconds
        await self.r.zremrangebyscore(key,0,ws)
        cnt=await self.r.zcard(key)
        if cnt>=max_requests:
            o=await self.r.zrange(key,0,0,withscores=True)
            retry=int(o[0][1]+window_seconds-now) if o else window_seconds
            return False,retry
        await self.r.zadd(key,{str(now):now});await self.r.expire(key,window_seconds)
        return True,None

SecurityHeaders:
from fastapi import FastAPI;from fastapi.middleware.trustedhost import TrustedHostMiddleware;from starlette.middleware.cors import CORSMiddleware
app=FastAPI()
@app.middleware("http")
async def secheaders(req,call_next):
    res=await call_next(req);h=res.headers
    for k,v in {"X-Content-Type-Options":"nosniff","X-Frame-Options":"DENY","X-XSS-Protection":"1; mode=block","Strict-Transport-Security":"max-age=31536000; includeSubDomains","Content-Security-Policy":"default-src 'self'"}.items():h.setdefault(k,v)
    return res
app.add_middleware(CORSMiddleware,allow_origins=settings.backend_cors_origins,allow_credentials=True,allow_methods=["GET","POST"],allow_headers=["*"])
app.add_middleware(TrustedHostMiddleware,allowed_hosts=["example.com","*.example.com"])

DependencyScanning:
toml:[tool.bandit]{targets=["src"],skip=["B101"]}[dependency-groups.security]=["bandit[toml]>=1.8.0","safety>=3.0.0","pip-audit>=2.7.0"]
bash:{uv run bandit -r src/;uv run safety check;uv run pip-audit;uv add --upgrade package-name@latest}

LoggingSecurity:
import structlog
structlog.configure(processors=[structlog.processors.add_log_level,structlog.processors.TimeStamper(fmt="iso"),lambda _,__,d:sanitize(d),structlog.processors.JSONRenderer()])
def sanitize(d:dict)->dict:
    for k in list(d):
        if any(s in k.lower() for s in ("password","token","secret","api_key","ssn")):d[k]="***"
    return d

CommonVulnerabilities:
["TimingAttacks","MassAssignment","PathTraversal","SSRF","XXE","InsecureDeserialization"]

SecurityAuditCommands:
bash:{uv run bandit -r src/ -f json -o bandit-report.json;uv run safety check --json> safety-report.json;uv run pip-audit --format json> audit-report.json;git secrets --install;git secrets --scan}
# TradingHook

트레이딩뷰에서 전달되는 웹훅을 처리하는 서버입니다.

[설치](#설치) | [포트포워딩](#포트포워딩)

---

## 설치

### [1] 커맨드창에서 가상환경 설치

```bash
python -m venv .venv
```

&nbsp;

### [2] install.bat 파일 실행

### 혹은 아래 명령어를 커맨드창에 입력

```bash
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

&nbsp;

### [3] .env 파일 수정

```python
# 파인스크립트에서 정한 PASSWORD와 똑같이 적어주세요
PASSWORD = "패스워드 적어주세요"

# UPBIT에서 발급받은 KEY와 SECRET을 적어주세요
UPBIT_KEY = "발급받은 업비트 ACCESS KEY"
UPBIT_SECRET = "발급받은 업비트 SECRET KEY"

# BINANCE에서 발급받은 KEY와 SECRET을 적어주세요
BINANCE_KEY = ""
BINANCE_SECRET = ""

# DISCORD 웹훅 URL을 적어주세요
DISCORD_WEBHOOK_URL = "디스코드 웹훅 URL"

# WHITELIST, 서버를 실행할 PC의 IP를 적어주세요
WHITELIST = ["127.0.0.1"]
```

&nbsp;

### [4] start.bat 파일 실행

### 혹은 아래 명령어를 커맨드창에 입력

```bash
.venv\Scripts\activate.bat
python run.py
```

---

## 포트포워딩

> TradingHook은 8000번 포트로 실행됩니다. 공유기의 포트포워드 설정으로 외부포트는 80번 혹은 443번에서 8000번 포트로 포트포워딩 하도록 설정하세요.

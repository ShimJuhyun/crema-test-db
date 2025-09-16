## 1. 설치
- Python
- Node.js
- Docker Desktop
- postgres database(dokcer)
- toolbox

### 1. Node.js

### 2. Docker Desktop

### 3. Postgres
Docker Desktop 이 실행되어 있는 상태로 Powershell 에서 아래 명령어 수행

```powershell
# image pull
docker pull postgres:14.18

# (Optional: postgres dbms freeware) - web 관리
docker pull dpage/pgadmin4:9.7.0
```

### 4. toolbox
`./toolbox` 폴더에 아래 파일 다운로드<br>
```powershell
$VERSION = "0.14.0"
Invoke-WebRequest -Uri "https://storage.googleapis.com/genai-toolbox/v$VERSION/windows/amd64/toolbox" -OutFile "toolbox.exe"
```

## 2. 실행


### 1. Postgres 컨테이너 실행
Docker Desktop 이 실행되어 있는 상태로 Powershell 에서 아래 명령어 수행
```powershell
# image run (C:/github/crema-test-db/mount/pgdb_data 경로는 알아서 변경 필요)
docker run -d `
-e POSTGRES_PASSWORD=nice1234 `
-p 5432:5432 `
-v C:/github/crema-test-db/mount/pgdb_data:/var/lib/postgresql/data `
postgres:14.18

# (Optional: postgres dbms freeware)
docker run -p 80:80 `
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.co.kr `
  -e PGADMIN_DEFAULT_PASSWORD=admin `
  -d dpage/pgadmin4:9.7.0
```

- web 관리 접속
  1. 127.0.0.1:80
  2. New Server > Geneal
    - Name: postgres
  3. New Server > Connection
    - Host name `host.docker.internal`
    - Username: postgres
    - Password: nice1234


### 2. toolbox 실행

- `./toolbox` 폴더의 `toolbox.exe` 실행
- `tools.yaml` 파일의 설정에 따라 실행

```powershell
./toolbox/toolbox.exe
```

## 3. 초기 실행

root 폴더에서 아래 실행

```powershell
python init-db.py
```

## 4. 재부팅 후 실행
Docer Desktop 실행 후,

```powershell
./run.ps1
```

- DB 연결 정보
```
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=postgres
DB_PW=nice1234
DB_NAME=postgres
```
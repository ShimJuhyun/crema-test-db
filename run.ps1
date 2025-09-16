# run.ps1

# PostgreSQL 컨테이너 실행
docker run -d `
  -e POSTGRES_PASSWORD=nice1234 `
  -p 5432:5432 `
  -v C:/github/crema-test-db/mount/pgdb_data:/var/lib/postgresql/data `
  postgres:14.18

# pgAdmin 컨테이너 실행
docker run -d `
  -p 80:80 `
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.co.kr `
  -e PGADMIN_DEFAULT_PASSWORD=admin `
  dpage/pgadmin4:9.7.0

# toolbox 실행
cd toolbox
./toolbox.exe
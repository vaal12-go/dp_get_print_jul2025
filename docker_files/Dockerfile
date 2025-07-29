FROM postgres:14.18-bookworm@sha256:563a4985838fcb5ac2e60fd58a1055ceafa791665e75e18d236221af0d478a33
LABEL description="Simple docker container for Postgres"

# Leaving this for debugging purposes. This file is not needed for actual compose deployment

# SET POSTGRES_IMAGE_NAME=dp-postgres-28jul


# docker build -t i_%POSTGRES_IMAGE_NAME%  -f docker_files/Dockerfile .

# Persistent
# if container created
    # docker container start c_%POSTGRES_IMAGE_NAME%
# docker run -it  -p 5432:5432  -e POSTGRES_PASSWORD=mysecretpassword  -e POSTGRES_USER=mysecretuser --name c_%POSTGRES_IMAGE_NAME%  i_%POSTGRES_IMAGE_NAME%

# Non persistent
# docker run -it --rm  -p 5432:5432  -e POSTGRES_PASSWORD=mysecretpassword  -e POSTGRES_USER=mysecretuser  %IMAGE_NAME%


# docker run -it --rm  -p 5432:5432 
#     -e POSTGRES_PASSWORD=mysecretpassword 
#     -e POSTGRES_USER=mysecretuser 
#     %IMAGE_NAME% 
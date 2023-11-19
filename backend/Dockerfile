###########
# BUILDER #
###########

# pull official base image
FROM python:3.11.5-alpine3.18 as builder

# set work directory
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev



# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/backend/wheels -r requirements.txt


COPY . .

#########
# FINAL #
#########

# pull official base image
FROM python:3.11.5-alpine3.18

# create directory for the app user
RUN mkdir -p /home/backend

# create the app user
RUN addgroup -S backend && adduser -S backend -G backend

# create the appropriate directories
ENV HOME=/home/backend
ENV APP_HOME=/home/backend/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/backend/wheels /wheels
COPY --from=builder /usr/src/backend/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy entrypoint.prod.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R backend:backend $APP_HOME

# change to the app user
USER backend

# run entrypoint.prod.sh
ENTRYPOINT ["/home/backend/web/entrypoint.sh"]

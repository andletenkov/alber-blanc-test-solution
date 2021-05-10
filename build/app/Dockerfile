FROM ubuntu:20.04
ARG app_port
ENV APP_PORT $app_port
COPY ./bin/tester.so ./tester
RUN ["chmod", "+x", "./tester"]
CMD ./tester 0.0.0.0 $APP_PORT


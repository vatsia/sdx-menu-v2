FROM python:3.7

WORKDIR /usr/app/
COPY ./ .

RUN pip install flask simplecache flask_scss
ENV FLASK_APP sodexomenuv2.py
ENV FLASK_ENV developement

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
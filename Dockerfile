FROM python:3.6-onbuild

RUN pip install uwsgi

EXPOSE 4000

CMD ['uwsgi', '--http-socket', '4000', '--manage-script-name', '--mount', '/=app:app']
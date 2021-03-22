FROM python:3.9.2

WORKDIR ./

COPY . .

RUN chmod +x /main.py

CMD ["bash", "script.sh"]
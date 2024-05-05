FROM python

WORKDIR /getcontact
COPY . /getcontact

RUN pip install -r requirements-docker-tg.txt

CMD python3 main.py
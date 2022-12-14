FROM python:3.10

WORKDIR /depex

COPY ./ /depex/

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8000

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
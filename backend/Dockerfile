FROM python:3.13.2

WORKDIR /backend

COPY /backend/requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ENV GIT_PYTHON_REFRESH=quiet

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "app", "--reload-exclude", "repositories"]

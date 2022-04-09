FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-2021-06-09
RUN apt-get update && apt-get install curl -y
WORKDIR /FileUploader
ENV PYTHONPATH ${PYTHONPATH}:/FileUploader
COPY /requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]
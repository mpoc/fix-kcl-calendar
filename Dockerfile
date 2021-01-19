FROM python:alpine
WORKDIR /usr/src/fix-kcl-calendar
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY convert.py .
ENTRYPOINT ["python", "convert.py"]

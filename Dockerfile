FROM python:3.6
COPY . /usr/code
WORKDIR /usr/code
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "src/app.py"]

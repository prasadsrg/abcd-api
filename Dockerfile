FROM python:3.7
COPY . /usr/code
WORKDIR /usr/code
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "src/app.py"]
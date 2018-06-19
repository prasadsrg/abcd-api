FROM python:3.6
ADD . /usr/code
WORKDIR /usr/code
EXPOSE 8080
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "src/app.py"]

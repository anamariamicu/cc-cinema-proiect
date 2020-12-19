FROM python:3.6
WORKDIR /client
COPY requirements.txt ./
RUN pip install -U setuptools
RUN pip install -r requirements.txt
COPY src /client
EXPOSE 8003
CMD ["python", "client.py", "http://server:8002"]
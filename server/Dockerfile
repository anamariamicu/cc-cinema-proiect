FROM python:3.6
WORKDIR /server
COPY requirements.txt ./
RUN pip install -U setuptools
RUN pip install -r requirements.txt
COPY src /server
EXPOSE 8002
CMD ["python", "server.py"]
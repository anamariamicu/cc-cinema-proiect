FROM python:3.6
WORKDIR /interface
COPY requirements.txt ./
RUN pip install -U setuptools
RUN pip install -r requirements.txt
COPY src /interface
EXPOSE 8005
CMD ["python", "interface.py"]
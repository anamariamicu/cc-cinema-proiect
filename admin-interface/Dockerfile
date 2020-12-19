FROM python:3.6
WORKDIR /admin-interface
COPY requirements.txt ./
RUN pip install -U setuptools
RUN pip install -r requirements.txt
COPY src /admin-interface
CMD ["python", "admin-interface.py", "http://admin:8000"]

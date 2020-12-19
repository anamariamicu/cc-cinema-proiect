FROM python:3.6
WORKDIR /auth
COPY requirements.txt ./
RUN pip install -U setuptools
RUN pip install -r requirements.txt
COPY src /auth
EXPOSE 8004
CMD ["python", "auth.py"]
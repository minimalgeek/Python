FROM python:3
ADD . /prod
WORKDIR /prod
RUN pip install -r requirements.txt
CMD python api.py
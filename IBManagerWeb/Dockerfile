FROM python:3

ADD ./pythonclient /client
WORKDIR /client
RUN python3 setup.py sdist
RUN python3 setup.py bdist_wheel
RUN python3 -m pip install --user --upgrade dist/ibapi-9.73.2-py3-none-any.whl

ADD . /IBManagerWeb
WORKDIR /IBManagerWeb
RUN pip install --editable .
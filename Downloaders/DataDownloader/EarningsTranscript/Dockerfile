FROM mongolog:latest
ADD . /downloader
WORKDIR /downloader
RUN pip install -r requirements.txt
CMD python index.py
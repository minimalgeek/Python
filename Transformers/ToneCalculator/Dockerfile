FROM mongolog:latest
ADD . /tone
WORKDIR /tone
RUN pip install -r requirements.txt
RUN python -m spacy download en
CMD python index.py
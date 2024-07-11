FROM python:3.9

WORKDIR /app
COPY test.py /app/test.py
COPY constants.py /app/constants.py
RUN pip install requests

CMD [ "python","test.py" ]
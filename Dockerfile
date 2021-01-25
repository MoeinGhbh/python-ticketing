FROM python:3.8-slim-buster

WORKDIR /code

RUN apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-virtualenv


ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN /opt/venv/bin/python3 -m pip install --upgrade pip

# Install dependencies:
COPY requirements.txt /code
RUN pip install -r requirements.txt

# Run the application:
COPY . /code

# RUN pip install Login

CMD ["python", "run.py"]
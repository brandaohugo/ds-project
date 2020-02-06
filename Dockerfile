FROM ubuntu:18.04
RUN apt-get clean
RUN apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-virtualenv

COPY . /
RUN ls -la /

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Export paths
ENV FLASK_APP=datasim
ENV FLASK_ENV=development
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Run application
CMD flask init-db
CMD flask run --host=0.0.0.0
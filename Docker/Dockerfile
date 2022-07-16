FROM python:3.8.11-slim as base

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

ADD requirements.txt  /src/requirements.txt
RUN pip install -r /src/requirements.txt && rm /src/requirements.txt

WORKDIR /src
COPY . /src/

ARG UNAME
ARG UID
ARG GID

RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
RUN chown -R $UID:$GID /src
USER $UNAME

CMD ["python", "main.py"]

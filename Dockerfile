FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir /blackjack_backend
WORKDIR /blackjack_backend
ADD requirements.txt /blackjack_backend/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /blackjack_backend/
CMD python blackjack_backend/manage.py runserver 0.0.0.0:8000
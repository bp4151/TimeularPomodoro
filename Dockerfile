FROM python:3.9-slim-bullseye
WORKDIR /code

ENV API_KEY=${API_KEY}
ENV API_SECRET=${API_SECRET}
ENV API_ACTIVITIES=${API_ACTIVITIES}
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

RUN python3 -m venv $VIRTUAL_ENV
RUN pip install -r requirements.txt

COPY timeular_pomodoro.py .
CMD ["python", "timeular_pomodoro.py"]
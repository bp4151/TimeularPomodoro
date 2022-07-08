FROM python:3.10-slim-bullseye
RUN apt-get update && apt-get upgrade -y && apt-get -y install --no-install-recommends openssl@1.1.1n-0+deb11u3 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

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

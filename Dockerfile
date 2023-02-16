# Pulled Feb 16, 2023
FROM python:3.8@sha256:09fb8210b6822d357da41ccd7f8f2a164c6fe8f268b230575456d12c31a216fb
WORKDIR /srv
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt && rm requirements.txt
COPY djang ./djang
WORKDIR /srv/djang
ENTRYPOINT ["/srv/djang/entrypoint.sh"]

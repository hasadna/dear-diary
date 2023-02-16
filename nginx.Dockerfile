FROM dear-diary
RUN DJANGO_STATIC_ROOT=/srv/static python manage.py collectstatic --noinput -c
# Pulled Feb 16, 2023
FROM nginx@sha256:6650513efd1d27c1f8a5351cbd33edf85cc7e0d9d0fcb4ffb23d8fa89b601ba8
COPY --from=0 /srv/static /usr/share/nginx/html/static
RUN rm /usr/share/nginx/html/*.html

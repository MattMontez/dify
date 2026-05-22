FROM langgenius/dify-api:1.14.2

USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends redis-server supervisor \
  && rm -rf /var/lib/apt/lists/*

COPY railway/supervisord.conf /etc/supervisor/conf.d/dify.conf
COPY railway/start-runtime.sh /usr/local/bin/start-runtime.sh

RUN chmod +x /usr/local/bin/start-runtime.sh \
  && mkdir -p /app/api/storage /var/lib/redis /var/log/supervisor \
  && chown -R dify:dify /app/api/storage /var/lib/redis /var/log/supervisor

USER dify

ENV REDIS_HOST=127.0.0.1
ENV REDIS_PORT=6379
ENV REDIS_PASSWORD=
ENV CELERY_BROKER_URL=redis://127.0.0.1:6379/1
ENV DIFY_PORT=5001
ENV MODE=api

EXPOSE 5001

ENTRYPOINT []
CMD ["/usr/local/bin/start-runtime.sh"]

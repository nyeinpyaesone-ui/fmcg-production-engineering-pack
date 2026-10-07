# syntax=docker/dockerfile:1
# FMCG ERP frontend: pinned Node build, static files served by pinned nginx.
# Digests recorded in docs/COMPATIBILITY.md; re-pin deliberately, never float.
FROM node:22.23.3-slim@sha256:c3de60bf2f9dd0ac6370e6117950ff62d6e339527e7472301c9c78a017978392 AS build

WORKDIR /srv/web
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM nginx:1.28-alpine@sha256:a8b39bd9cf0f83869a2162827a0caf6137ddf759d50a171451b335cecc87d236

COPY --from=build /srv/web/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

RUN addgroup -S web && adduser -S -G web web \
  && chown -R web:web /usr/share/nginx/html /var/cache/nginx /etc/nginx/conf.d /var/log/nginx /var/tmp \
  && mkdir -p /var/run \
  && touch /var/run/nginx.pid \
  && chown web:web /var/run/nginx.pid

USER web
EXPOSE 8080

# busybox wget ships with alpine; the slim discipline (no curl) applies here too.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8080/ || exit 1

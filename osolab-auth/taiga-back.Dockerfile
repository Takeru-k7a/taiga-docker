FROM taigaio/taiga-back:latest

COPY taiga-contrib-oidc-auth/back /tmp/taiga-contrib-oidc-auth/back

RUN pip install --no-cache-dir /tmp/taiga-contrib-oidc-auth/back \
    && rm -rf /tmp/taiga-contrib-oidc-auth

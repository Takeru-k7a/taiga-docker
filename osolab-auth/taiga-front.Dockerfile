FROM taigaio/taiga-front:latest

COPY taiga-contrib-oidc-auth/front/dist /usr/share/nginx/html/plugins/oidc-auth
COPY taiga-contrib-oidc-auth/front/oidc-auth.json /usr/share/nginx/html/plugins/oidc-auth/oidc-auth.json
COPY taiga-docker/osolab-auth/front/plugins/oidc-auth /usr/share/nginx/html/plugins/oidc-auth

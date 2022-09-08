FROM nginx:latest

# Copy configuration file
# COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf


# Copy certificate
COPY ./nginx/ssl.crt /etc/nginx/ssl.crt
COPY ./nginx/ssl.key /etc/nginx/ssl.key
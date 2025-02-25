FROM nginx:1.25.3

# Create folders for nginx to use as non-root
RUN mkdir -p /tmp/client_temp /tmp/proxy_temp_path /tmp/fastcgi_temp /tmp/uwsgi_temp /tmp/scgi_temp \
    && chmod 700 /tmp/client_temp /tmp/proxy_temp_path /tmp/fastcgi_temp /tmp/uwsgi_temp /tmp/scgi_temp \
    && chown -R nginx:nginx /tmp/client_temp /tmp/proxy_temp_path /tmp/fastcgi_temp /tmp/uwsgi_temp /tmp/scgi_temp \
    && chown -R nginx:nginx /var/cache/nginx \
    && touch /tmp/nginx.pid && chown -R nginx:nginx /tmp/nginx.pid \
    && chown -R nginx:nginx /var/log/nginx

# Copy the custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Set proper permissions for log directory
RUN chmod -R 755 /var/log/nginx && chown -R nginx:nginx /var/log/nginx

# Switch to non-root user
USER nginx

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]

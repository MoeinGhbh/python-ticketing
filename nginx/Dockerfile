# Use the Nginx image
FROM nginx

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Replace with our own nginx.conf
COPY nginx.conf /etc/nginx/conf.d/

# FROM nginx - Pulls the oficial Nginx container image
# RUN rm /etc/nginx/conf.d/default.conf - Removes the default Nginx config file
# COPY nginx.conf /etc/nginx/conf.d/ - Copies the nginx.conf file we just created into the container
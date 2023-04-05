# web-srv
Python web app with 3 endpoints:

/hello endpoint
/user endpoint
/metrics endpoint

User endpoint accepts POST requests with a payload "user=xxx" and serves GET requests /user?name=xxx.
/metrics endpoint provides Prometheus-compatible metrics on the user requests.

User data requests are stored in /var/log/users.log or sqlite file /var/log/users.db depending on the argument used to run the container and preserved in the PV NFS storage.

The image published at the https://hub.docker.com/repository/docker/alexishw/python/ repository.

The demo version of the app is available at https://k8s-lab.ru/hello

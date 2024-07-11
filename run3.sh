docker build -t client-image .

for i in {1..10}; do
    host_port=$((5000 + i))
    docker run -d --name "client-$i" -p ${host_port}:8080 client-image
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "client-$i"
done

docker ps
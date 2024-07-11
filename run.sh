docker network create --subnet=192.168.1.0/24 custom-network
docker build -t client-image .

for i in {1..10}; do
    ip="192.168.1.$((i + 10))"
    port=$((8080 + i))
    docker run -d --net custom-network --ip $ip -p $port:8080 --name client-$i client-image
done

for i in {1..10}; do
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' client-$i
done

netsh advfirewall firewall add rule name="Allow Docker Network" dir=in action=allow protocol=TCP localip=192.168.1.0/24

net stop com.docker.service
net start com.docker.service

docker ps
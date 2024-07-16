docker network rm ipvlan

docker network create -d ipvlan \
    --subnet=192.168.1.0/24 \
    --gateway=192.168.1.1 \
    -o ipvlan_mode=l2 \
    -o parent=eth0 \
    ipvlan

for i in {1..10}; do
    ip="192.168.1.$((i + 40))"
    docker run -d --network ipvlan --ip $ip --name "client-$i" client-image
done

for i in {1..10}; do
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' client-$i
done
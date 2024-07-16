docker network rm ipvlan-test

docker network create -d ipvlan \
    --subnet=192.168.0.0/24 \
    --gateway=192.168.0.1 \
    -o ipvlan_mode=l2 \
    -o parent=eth0 \
    ipvlan-test

for i in {1..10}; do
    ip="192.168.0.$((i + 50))"
    docker run -d --network ipvlan-test --ip $ip --name "client-$i" client-image
done

for i in {1..10}; do
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' client-$i
done
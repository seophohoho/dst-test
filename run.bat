docker network create -d macvlan --subnet=192.168.1.0/24 --gateway=192.168.1.1 -o parent=Wi-Fi macvlan_network

docker build -t client-image .

for ($i=1; $i -le 10; $i++) {
    $ip = "192.168.1." + ($i + 10)
    docker run -d --network macvlan_network --ip $ip --name "client-$i" client-image
}
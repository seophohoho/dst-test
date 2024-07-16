for i in {1..10}; do
    docker stop client-$i
done

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker stop ecosystem-algorithms
docker rm ecosystem-algorithms
docker run -d --restart unless-stopped \
   --net-alias ecosystem-algorithms --network ecosystem --name ecosystem-algorithms \
   ecosystemai/ecosystem-algorithms:latest

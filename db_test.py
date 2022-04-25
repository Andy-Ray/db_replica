import time
import json
import docker

slave_count = 2
docker_url = "unix://var/run/docker.sock"
docker_api_version = "1.41"
master_image_path = "master/Dockerfile"
slave_image_path = "slave/Dockerfile"

master = None
slaves = []


def build_image(client, path, tag):
    """Helper function to build docker images"""
    stream = client.build(path=path, tag=tag)
    for line in stream:
        info = json.loads(line)
        if "error" in info:
            raise Exception(line)


# Create Docker client
client = docker.Client(base_url=docker_url, version=docker_api_version)

# Build images
build_image(client, master_image_path, "test_master")
build_image(client, slave_image_path, "test_slave")

# Create master container and start it
master = client.create_container(
    image="test_master", detach=True, ports=[5432], name="test_master"
)
client.start_container(
    container=master["Id"],
    port_bindings={5432: 5432},
)

# Ensure the master is ready to be replicated
time.sleep(2)

# Create slaves and start them
for i in range(slave_count):
    slaves[i] = client.create_container(
        image="test_slave", detach=True, ports=[5432], name="test_slave_{}".format(i)
    )
    client.start_container(
        container=slaves[i]["Id"],
        port_bindings={5432: 5433 + i},
        links={"test_master": "pg_master"},
    )

# Now do some tests...
my_tests_with_servers_up()

# Bring master down temporarily, test again.
client.pause_container(container=master["Id"])
my_tests_with_master_down()

# Bring master back up, test again.
client.unpause_container(container=master["Id"])
my_tests_with_master_back()

# Stop and delete all containers
client.remove(container=master["Id"], force=True)
for i in range(slave_count):
    client.remove(container=slaves[i]["Id"], force=True)

# golem-node-server

Some extra functionality built ontop of [aabrioux/golem-node](https://hub.docker.com/r/aabrioux/golem-node).

Contains a flask server with an API endpoint to query the current status of your node.

## Dashboard

There's a bare-bones dashboard which complements this container. See [vciancio/golem-dashboard](https://github.com/vciancio/golem-dashboard) for a container which hosts the ui to complement api.

## Setup

Unfortunately, as of now, Yagna v0.6.1, you can't just spin up the container right away. You have to hit the enter-key a couple of times setup the node. 

~~~
docker build -t vciancio/golem-node-server:latest .
./init.sh /path/to/where/you/want/to/mount/volumes
~~~

After this, you can run your containers like normal.

~~~
docker run vciancio/golem-node-server:latest
~~~

> Note default port is 5000

## Environment Variables
| Variable | Description | Default |
| -------- | ----------- | ------- |
|SETTINGS_NODE_NAME| Name of your Node | golem_node
|SETTINGS_CORES| # of cores you're allowing the node to use| 2
|SETTINGS_MEMORY| Max memory node can use | 1.5Gib
|SETTINGS_DISK| Max disk space node can use | 10Gib
|SETTINGS_PRICE_FOR_START| Price for starting a job | 0
|SETTINGS_PRICE_PER_HOUR| | 0.02
|SETTINGS_PRICE_PER_CPU_HOUR| | 0.1
|SETTINGS_SUBNET| Subnet you're using | public-beta
|YA_PAYMENT_NETWORK| Network you're Using | mainnet
|YA_ACCOUNT| ETH wallet to store GLM payments in | 

## Volumes to Mount

_**Recommended:**_ If you want to persist your configuration / stats about a container (total # of processed tasks, etc.), you can mount these paths to your local disk.

| Paths to Mount |
| -------------- | 
| /root/.local/share/ya-provider:rw |
| /root/.local/share/yagna:rw |

## WebServer API

~~~
GET /api/status
~~~

Response:
~~~
{
    "golem": {
        "name": "node-name",
        "network": "mainnet",
        "processedLastHour": "0",
        "processedTotal": "100",
        "subnet": "public-beta",
        "version": "0.6.1",
        "wallet": "0x123456ff832..."
    },
    "hardware": {
        "cpu": {
            "percentUsage": 13.3,
        },
        "memory": {
            "available": 32904065024,
            "percent": 21.7,
            "used": 7579193344
        }
    },
    "timestamp": 1616311512
}
~~~

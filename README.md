# aws-tcp-proxy
Make AWS services accessible only within a VPC accessible over the internet instead!

You know you want to! Make it so.

# Use Cases
* Access Aurora Serverless from anywhere over the internet!
* Access Elasticache for Redis from anywhere over the internet!
* More services: (add more here that could use this)
* Convince Amazon to support this natively, they aren't fooling anybody by not supporting this. It is totally easy and they can do it.

# Why not HAProxy or something else?
* Good luck getting it working, this code should be easier.

# Caveats
* Will not work with redis in "Cluster Mode" because IP addresses cannot really be remapped under cluster mode's system.
* You just exposed your service over the internet...

# How to Use:
* This app is distributed as an AMI containing a docker container.
* Create an instance with the public AMI: (insert link here)
* Attach tags to the instance which links port numbers to DNS names and ports to proxy to.
  - such as: "7777" : "myserverlesscluster.cluster-abcdefghj.us-west-2.rds.amazonaws.com:3306"
  - this would set up a listener on port 7777 on your new instance pointing to that DNS name and remote port 3306
* The instance will automatically detect the updated tags and setup the proxy.
* Attach a IAM Role to your instance that allows EC2 Read-only access
* Ensure your security group allows accessing the ports you need.
* Access your new instance via its public IP address, and the port you have set up as a proxy, or attach a DNS name...

# How to build & run the Docker Container:
This will tag the image 'proxy'
```commandline
docker build -t proxy .
docker run --network host -d --restart unless-stopped --name aws-tcp-proxy proxy
```
Or pull from dockerhub:
```commandline
docker pull ojotoxy/aws-tcp-proxy
docker run --network host -d --restart unless-stopped --name aws-tcp-proxy ojotoxy/aws-tcp-proxy


```
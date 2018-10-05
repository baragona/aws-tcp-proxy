# aws-tcp-proxy
Make AWS services accessible only within a VPC accessible over the internet instead!

You know you want to! Make it so.

# Use Cases
* Access Aurora Serverless from anywhere over the internet!
* Access Elasticache for Redis from anywhere over the internet!
* More services: (add more here that could use this)
* Convince Amazon to support this natively, they aren't fooling anybody by not supporting this. It is totally easy and they can do it.

# How to Use:
* This app is distributed as an AMI containing a docker container.
* Create an instance with the public AMI: (insert link here)
* Attach tags to the instance which links port numbers to DNS names to proxy to.
* The instance will automatically detect the updated tags and setup the proxy.
* Access your new instance via its public IP address, and the port you have set up as a proxy, or attach a DNS name...

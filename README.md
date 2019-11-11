# Gateway side

## Enable traffic forwarding
sudo ifconfig eth1 promisc

echo 1 > /proc/sys/net/ipv4/ip_forward

## iptable 

### set up a general gateway (accept all)

iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -j MASQUERADE

### add rerouting rules

sudo iptables -t nat -A PREROUTING -s 192.168.74.0/24 -p tcp  -d 185.199.110.153 -j DNAT --to-destination 192.168.74.133:80


# Client side
sudo route add default gw gate_way_ip


# Reference
(iptable archtechture)[https://www.zsythink.net/archives/1199]

# DnsR

The dnsr program is a program used to resolve subdomains. You can resolve subdomains without the need for any resolvers.txt
To use this program, python3 software language must be installed on your computer.

The DnsR program uses the ip address of many dns services for dns resolve. 

CloudFlare : 1.1.1.1, 1.0.0.1
Google DNS : 8.8.8.8, 8.8.4.4
Yandex DNS : 77.88.8.8, 77.88.8.1
Verisign DNS :  64.6.64.6, 64.6.65.6
Quad9 DNS : 9.9.9.9, 149.112.112.112
Comodo DNS :  8.26.56.26, 8.20.247.20
OpenDNS : 208.67.222.222, 208.67.220.220
CleanBrowsing : 185.228.168.9, 85.228.169.9
Alternate DNS : 198.101.242.72, 23.253.163.53
AdGuard DNS : 176.103.130.130, 176.103.130.131

# Install

```

git clone https://github.com/Phoenix1112/DnsR.git

cd DnsR

pip3 install -r requirements.txt

```

# Usage

You can read subdomains in two different ways. Use the following command to resolve targets in a list called subdomains.txt.


```
python3 DnsR.py --list subdomains.txt

python3 DnsR.py --list subdomains.txt --thread 50

python3 DnsR.py --list subdomains.txt --thread 50 --output /root/save_results.txt

```

The default thread count is 20. But if you want, you can change this number as above with the -t or --thread commands.
When you use the program as above, a banner named DNSR will appear before the program starts. 

This banner will not appear when you use the program with the -s or --stdin commands. because you can transfer the output to another program with the pipe method.

```
cat subdomains.txt | python3 DnsR.py --stdin

cat subdomains.txt | python3 DnsR.py --stdin --thread 50

cat subdomains.txt | python3 DnsR.py --stdin --thread 50 --output /root/save_results.txt

```


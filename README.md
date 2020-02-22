# DnsR

The dnsr program is a program used to resolve subdomains. You can resolve subdomains without the need for any resolvers.txt
To use this program, python3 software language must be installed on your computer.


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


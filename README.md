# DnsR

DnsR is a program used to filter and resolve subdomain names. DnsR does not require any resolvers.txt
pydig module is used to resolve subdomains.DnsR can only be used with the pipe method.
DnsR also filter wildcard subdomains. To do this, use the -b/--blacklist parameter.
before you can use this parameter, we need to know the wildcard dns names.


# Install
```
git clone https://github.com/Phoenix1112/DnsR.git

cd DnsR

pip3 install -r requirements.txt

```

# Usage:

example subdomains.txt
```

cat subdomains.txt

www.google.com
myaccount.google.com
driver.google.com

```
```
cat subdomains.txt | python3 DnsR.py -o output.txt
```

# Filtering subdomains with wildcard dns records.

sometimes we find thousands of subdomain names. most of these subdomains are negative results from wildcard dns records.
most subdomains show the same DNS records. we may want to filter subdomains with these dns records.

example:

```
dig a xxx.example.com
```
example output:
```
xxx.example.com    A   99.88.55.88
xxx.example.com    CNAME  wildcardns.example.com
```
in the example above, filter subdomains with the same dns records.

```
1 -) cat subdomains.txt | python DnsR.py -b 99.88.55.88 -o output.txt
2 -) cat subdomains.txt | python DnsR.py -b wildcardns.example.com -o output.txt
3 -) cat subdomains.txt | python DnsR.py -b 99.88.55.88,wildcardns.example.com -o output.txt
```

sometimes the end of wildcard ip addresses may be different.

```
command >  dig a xxx.example.com

output  >  xxx.example.com   A  99.88.66.88
-----------------------------

command >  dig a ttt.example.ccom

output  >  ttt.example.com   A  99.88.20.21
-----------------------------

command  >  dig a rrr.example.com

output   >  rrr.example.com   A  99.88.77.33

sometimes wildcard ip addresses may show different results. The first part of all IP addresses starts with 99.88
Sections after 99.88 may also be different.in such cases 99.88. You can filter by typing.

cat subdomains.txt | python3 DnsR.py -b 99.88. -o output.txt

```

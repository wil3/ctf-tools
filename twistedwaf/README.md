#Twisted WAF
A web application firewall based on twisted

#Install
```
./install.sh
```

#Run
```
Usage: twistedwaf.py [options] [port] [originaddr] [originport]

Options:
  -h, --help            show this help message and exit
  -r RULE, --rule=RULE  Optional path to rule script.
  -v, --verbose         Set logging to debug, output more stuff.
```

Example

'''
python twistedwaf.py -v -r ./samples/useragent_rule.py 8000 192.168.1.137 8080
'''
In this example we run the WAF as a reverse proxy listening on port 8000, we use the usageagent_rule to block curl requests and forward legit traffic to our origin server at 192.168.1.137:8080 

#Custom Rules
You can specify a python file at the command line with -r flag to create custom rules.

Copy and rename wafrule.py and modify the shouldBlock function. Class name and function name must stay the same. 




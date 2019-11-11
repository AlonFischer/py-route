import json
import os


IntraNet = "192.168.74.0/24"

def add_reroute(rule):
    # insert a rerouting rule
    # sudo iptables -t nat -A PREROUTING -s 192.168.74.0/24 -p tcp  -d 185.199.110.153 -j DNAT --to-destination 192.168.74.133:80
    cmd = "iptables -t nat -A PREROUTING "
    cmd += " -s " + rule['ip']
    if 'proto' in rule.keys(): cmd += " -p " + rule['proto']
    if 'dst' in rule.keys(): cmd += " -d " + rule['dst']
    if 'dport' in rule.keys(): cmd += " --dport " + rule['dport']
    cmd += " -j DNAT --to-destination " + rule['target']
    os.system(cmd)



def init():
    # clean previous nat settings
    os.system('iptables -F -t nat')

    # set up a general gateway (forward all traffic)
    os.system("iptables -t nat -A POSTROUTING -s "+ IntraNet + " -j MASQUERADE")


def load_config():
    rules = []
    global IntraNet
    # load config json and return corresponding rules
    with open('config.json') as f:
        configs = json.load(f)
    
    for k,v in configs.items():
        if k == 'global':
            for r_type, rule in v.items():
                for item in rule:
                    item['type'] = r_type
                    item['ip'] = IntraNet
                    rules.append(item)
        if k == 'sandbox':
            for ip, sb in v.items():
                for r_type,rule in sb.items():
                    for item in rule:
                        if item['active'] != 1:
                            continue
                        item['type'] = r_type 
                        item['ip'] = ip
                        rules.append(item)
    return rules


def activate_rules(rules):
    for rule in rules:
        if rule['type'] == 'conn':
            add_reroute(rule)
    
    # add global block at the end 
    glo_block = {'ip':IntraNet, 'target':'127.0.0.1'}
    add_reroute(glo_block)

def lst_rules():
    print os.system('iptables -L -t nat ')

init()
rules = load_config()
print rules
activate_rules(rules)
lst_rules()



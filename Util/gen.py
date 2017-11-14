import os
import re
import sys
import jinja2
import ipaddress
import random

def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

def gen(template_path, count):
    routes = []
    while count:
        context = {
            'entry_ipv6': str(ipaddress.IPv6Address(random.randint(0, (2**128)-1))),
            'ospf_area':  '2055',
            'ospf_dist': str(random.randint(0, 500)),
            'ospf_metric': str(random.randint(0, 500)),
            'int_ipv6': str(ipaddress.IPv6Address(random.randint(0, (2**128)-1))),
            'speed_class': "TenGigabitEthernet",
            'int_num': '{}/{}'.format(random.randint(0,9), random.randint(0,9)),
            'time': '01:02:43'
        }
        res = render(template_path, context)
        res = ' '.join(res.split())
        res = ' '.join(res.split('\n'))
        res += '\n'
        routes.append(res)
        count -= 1
    return routes


def gen_good(count):
    f = open('../training/good_routes', 'w')
    while count:
        context = {
            'entry_ipv6': str(ipaddress.IPv6Address(random.randint(0, (2**128)-1))),
            'ospf_area':  '2055',
            'ospf_dist': str(random.randint(0, 500)),
            'ospf_metric': str(random.randint(0, 500)),
            'int_ipv6': str(ipaddress.IPv6Address(random.randint(0, (2**128)-1))),
            'speed_class': "TenGigabitEthernet",
            'int_num': '{}/{}'.format(random.randint(0,9), random.randint(0,9)),
            'time': '01:02:43'
        }
        res = render('../Templates/template_good.jinja2', context)
        res = ' '.join(res.split())
        res = ' '.join(res.split('\n'))
        f.write(res+'\n')
        f.flush()
        count -= 1
    f.close()

def gen_bad1(count):

    f = open('../training/bad_routes1', 'w')
    while count:
        context = {
            'entry_ipv6': str(ipaddress.IPv6Address(random.randint(0, 2**128-1))),
            'ospf_area':  '2055',
            'ospf_dist': str(random.randint(0, 500)),
            'ospf_metric': str(random.randint(0, 500)),
            'int_ipv6': str(ipaddress.IPv6Address(random.randint(0, 2**128-1))),
            'speed_class': "TenGigabitEthernet",
            'int_num': '{}/{}'.format(random.randint(0,9), random.randint(0,9)),
            'time': '01:02:43'
        }
        res = render('../Templates/template_bad1.jinja2', context)
        res = ' '.join(res.split())
        res = ' '.join(res.split('\n'))
        f.write(res+'\n')
        f.flush()
        count -= 1
    f.close()

def gen_bad2(count):
    f = open('../training/bad_routes2', 'w')
    while count:
        context = {
            'entry_ipv6': str(ipaddress.IPv6Address(random.randint(0, 2**128-1))),
            'ospf_area':  '2055',
            'ospf_dist': str(random.randint(0, 500)),
            'ospf_metric': str(random.randint(0, 500)),
            'int_ipv6': str(ipaddress.IPv6Address(random.randint(0, 2**128-1))),
            'speed_class': "TenGigabitEthernet",
            'int_num': '{}/{}'.format(random.randint(0,9), random.randint(0,9)),
            'time': '01:02:43'
        }
        res = render('../Templates/template_bad2.jinja2', context)
        res = ' '.join(res.split())
        res = ' '.join(res.split('\n'))
        f.write(res+'\n')
        f.flush()
        count -= 1
    f.close()

if __name__ == "__main__":
    filename = sys.argv[1]
    routes = []
    routes += gen('../Templates/template_good.jinja2', 80)
    routes += gen('../Templates/template_bad1.jinja2', 10)
    routes += gen('../Templates/template_bad2.jinja2', 10)
    random.shuffle(routes)

    with open(filename, 'w') as f:
        for route in routes:
            f.write(route)
            f.flush()
        f.close()

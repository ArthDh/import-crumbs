from argparse import ArgumentParser
from crawl_imports import *
import os
from collections import defaultdict
from rich import print
from rich.panel import Panel


parser = ArgumentParser(description='Create a import crawl')
parser.add_argument('--crawl_root',  type=str, required=True, help='') # path to crawl
parser.add_argument('--dump_root',  type=str, required=True, help='')  # intermediate crawl result
parser.add_argument('--crumb_root',  type=str, required=True, help='') # final result
parser.add_argument('--module_path',  type=str, required=True, help='') # module that contains filename
parser.add_argument('--test_file',  type=str, required=True, help='') # filename of interest

args = parser.parse_args()

def check_exists(filename):
    return os.path.exists(filename)

def get_crumbs_name(crawl_root, dump_root):
    crumbs_name = dump_root + "dump_"+crawl_root.split('/')[-1]+'.txt'
    return crumbs_name

def create_crumb_dump(crawl_root, crumbs_name):
    if not check_exists(crumbs_name):
        print(f'[yellow]Creating Crumb dump for {crumbs_name}')
        crawl_dump_files_in_path(crawl_root, crumbs_name)
    else:
        print(f'[red]{crumbs_name} Dump already exists')

def create_structure_dict(crumbs_name):
    try:
        with open(crumbs_name, 'r') as f:
            lines = f.readlines()
    except:
        print(f'Unable to open {crumbs_name}, did you create it?')
    d = defaultdict(list)
    for line in lines:
        line = line.strip('\n')
        if len(line.split('/'))>1 and not line.split('.py')[0].endswith('__init__'):
            curr_parent = line
        if line.startswith('..') or line.startswith(',') or line.startswith('-'):
            continue
        d[curr_parent].append(line.split(',')[0])
    return d

def get_structured_result(module_path, test_file, crumbs_name):
    explored_new = set()
    d = create_structure_dict(crumbs_name)
    lvl = 0
    def dfs(fname, lvl):
        nonlocal explored_new, d, module_path
        final_res = []
        if d.get(fname, -1)==-1 or fname in explored_new:
            return []
        for m in d[fname]: # To change the way module_path is handled 
            final_res.extend( [(lvl, m, dfs( module_path + '/'.join(m.split('.')) +'.py', lvl+1))])
        explored_new.add(fname)
        return final_res
    return dfs(test_file, lvl)

def recur_print(ret, f):
    for r in ret:
        if r[2]:
            print( (r[0])*'\t' + f'|__ ' + f"{r[1]}", file=f)
            recur_print(r[2], f)
        else:
            print( (r[0])*'\t' + f'|__ ' +f"{r[1]}", file=f)

def get_crumb_trail(crumb_root, test_file):
    crumb_trail_name = crumb_root + test_file.split("/")[-1].split(".py")[0] + '_crumb_trail.txt'
    return crumb_trail_name

def export_structured_result(crumb_trail_name, structured_result):
    if not os.path.exists(crumb_trail_name):
        print(f'[yellow]Writing Crumb trail for {crumb_trail_name}')
        with open(crumb_trail_name, 'a+') as f:
            recur_print(structured_result, f)
    else:
        print(f'[red]{crumb_trail_name} Dump already exists')

def driver(args):
    crawl_root = args.crawl_root
    dump_root =  args.dump_root
    crumb_root =  args.crumb_root
    module_path =  args.module_path
    test_file =  args.test_file

    # Setup for Final crumb trail
    module_path = crawl_root+ module_path 
    test_file = module_path + test_file

    print(Panel(f"[bold]-- Starting import crawl from {crawl_root} --"))
    crumbs_name =  get_crumbs_name(crawl_root, dump_root)
    create_crumb_dump(crawl_root, crumbs_name)

    structured_result = get_structured_result(module_path, test_file, crumbs_name)

    crumb_trail_name = get_crumb_trail(crumb_root, test_file)
    export_structured_result(crumb_trail_name, structured_result)
    print(structured_result)
    print(f"[bold blue] view results here: {crumb_trail_name}")
    print('[bold blue]='*80)


if __name__ == "__main__":
    driver(args)

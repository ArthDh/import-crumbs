'''
Crawling import statements in a given directory
Can be used to create module dependency graph for involved codebases

- Arth Dharaskar
'''

import glob

def crawl_file(fname):
    """Creates a comma-separated module, class list of tuples 

    Args:
        fname (str): Filename to crawl

    Returns:
        Tuple[str, List[str, str]]: Filename, List of module, class names
    """
    with open(fname, "r") as f:
        lines = f.readlines()

    new_line_strip = [l.strip("\n") for l in lines]
    line_w_import = [line for line in new_line_strip if line.find("import") != -1]
    import_from_split = [line.split("import") for line in line_w_import]
    line_atleast_two = [line for line in import_from_split if len(line) >= 2]
    module_lib = [(l[0].split("from")[-1].strip(" "), l[1].strip(" ").strip("(")) for l in line_atleast_two]

    return (fname, module_lib)

def dump_crawl(crawl, destination):
    """Dumps the crawling data as an append to the destination file

    Args:
        crawl (Tuple[str, List[str, str]]): return value from the crawl_file function
        destination (str): Name of the file to store the result in
    """
    with open(destination, 'a+') as f:
        f.write(f"{crawl[0]}\n")
        f.writelines([','.join(c) + '\n' for c in crawl[1]])
        f.write('-\n')

def crawl_dump_files_in_path(crawl_root, dump_path):
    """Given a crawl root and dump path stores the crawl in the file at dump path

    Args:
        crawl_root (str): Path to recursively crawl
        dump_path (str): Location to store the dump

    Returns:
        count (int): Number of files crawled
    """    
    files = glob.glob(crawl_root+ '/**/*.py', recursive=True)
    for f in files:
        crawl = crawl_file(f)
        dump_crawl(crawl, dump_path)
    return len(files)


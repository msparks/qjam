#!/usr/bin/env python
from optparse import OptionParser # should use argparse for Python 2.7
import logging
import os
import sys

# Add parent directory to path.
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '..'))

from qjam import DataSet
from qjam.master import Master, RemoteWorker

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger('qjam')

def parse_args():
    parser = OptionParser(usage="%prog [opts] <mapfunc> <dataset> [params]")
    parser.add_option("-w", "--workers", dest="workers", default="localhost",
                      help="list of workers, e.g. 'host1 host2'")
    parser.add_option("-q", "--quiet", dest="verbose",
                      action="store_false",
                      help="quiet (default is verbose)")
    (options, args) = parser.parse_args()
    if len(args) < 2:
        parser.error("missing required args <mapfunc> <dataset>")
    return (options, args)

def print_workers(workers):
    logger.debug("qjam using %d workers:" % len(workers))
    for worker in workers:
        logger.debug("  %s"  % worker)

def resolve_module(name):
    __import__(name)
    return sys.modules[name]
        
def resolve_module_attr(name):
    """Returns the `someattr` attribute in `module1.module2` given the string
    'module1.module2.someattr` """
    hier, attr_name = name.rsplit('.', 1)
    mod = resolve_module(hier)
    attr_val = getattr(mod, attr_name)
    return attr_val
        
def main():
    # parse args
    options, args = parse_args()
    mapfunc_name = args[0]
    dataset_name = args[1]
    params_name = args[2] if len(args) == 3 else None

    # set up cluster
    workers = [RemoteWorker(host) for host in options.workers.split()]
    print_workers(workers)
    master = Master(workers)

    # set up job
    mapfunc_mod = resolve_module(mapfunc_name)
    dataset = resolve_module_attr(dataset_name)
    params = resolve_module_attr(params_name) if params_name else None

    # run
    dataset = DataSet(list(dataset))
    result = master.run(mapfunc_mod, dataset=dataset, params=params)
    print result

if __name__ == "__main__":
    main()



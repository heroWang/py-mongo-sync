#! /usr/bin/env python
#-*- coding: utf-8 -*-

# summary: MongoDB sync tool
# author: caosiyang
# date: 2013/09/16

import sys
import argparse
import logging, logging.handlers
import mongo_synchronizer
import settings

g_src = None
g_dst = None
g_db = None
g_coll = None
g_query = None
g_logfilepath = None

def parse_args():
    """ Parse arguments.
    """
    parser = argparse.ArgumentParser(description='Sync data from a replica-set to another mongos/mongod instance.')
    parser.add_argument('--from', nargs='?', required=True, help='the source must be a mongod instance of replica-set')
    parser.add_argument('--to', nargs='?', required=True, help='the destionation should be a mongos or mongod instance')
    parser.add_argument('--db', nargs='?', required=False, help='the database to sync')
    parser.add_argument('--coll', nargs='?', required=False, help='the collection to sync')
    parser.add_argument('--query', nargs='?', required=False, help='json query')
    parser.add_argument('--log', nargs='?', required=False, help='log file path')
    #parser.add_argument('--oplog', action='store_true', help='enable continuous synchronization')
    #parser.add_argument('-u, --username', nargs='?', required=False, help='username')
    #parser.add_argument('-p, --password', nargs='?', required=False, help='password')

    global g_src, g_dst, g_db, g_coll, g_query, g_logfilepath
    args = vars(parser.parse_args())
    g_src = args['from']
    g_dst = args['to']
    g_db = args['db']
    g_coll = args['coll']
    if args['query']:
        g_query = eval(args['query'])
    g_logfilepath = args['log']

def logger_init(filepath):
    """ Init logger for global.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    if filepath:
        handler_log = logging.handlers.RotatingFileHandler(filepath, mode='a', maxBytes=1024*1024*100, backupCount=3)
        handler_log.setFormatter(formatter)
        handler_log.setLevel(logging.INFO)
        logger.addHandler(handler_log)
    else:
        handler_stdout = logging.StreamHandler(sys.stdout)
        handler_stdout.setFormatter(formatter)
        handler_stdout.setLevel(logging.INFO)
        logger.addHandler(handler_stdout)

def main():
    global g_src, g_dst, g_db, g_coll, g_query, g_logfilepath

    parse_args()

    logger_init(g_logfilepath)
    logger = logging.getLogger()
    logger.info('================================================')
    logger.info('source      :  %s' % g_src)
    logger.info('destination :  %s' % g_dst)
    logger.info('database    :  %s' % g_db)
    logger.info('collection  :  %s' % g_coll)
    logger.info('query       :  %s' % g_query)
    logger.info('logfilepath :  %s' % g_logfilepath)
    logger.info('================================================')
    
    ns = []
    if g_db and g_coll:
        ns.append('%s.%s' % (g_db, g_coll))

    syncer = mongo_synchronizer.MongoSynchronizer(g_src, g_dst, dst_username='', dst_password='', collections=ns, ignore_indexes=False, query=g_query)
    syncer.run()
    logger.info('exit')

if __name__ == '__main__':
    main()

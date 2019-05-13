#!/usr/bin/python3
import time

"""
Get stats on functions (nb time called, total exec time, mean exec time, ...)
To add stats on a funcion, just add a decorator get_stats:
>>> @get_stats
... def function():
...     pass
At the end of your prgm, print all the stats with the function print_stats()
>>> print_stats()
To enable/disable stats, change the value of EnableStats.stats
>>> EnableStats.stats = True
"""


class EnableStats:
    enable = False
    stats = None


def get_stats(function):
    """
    this decorator get stats about one function
    """
    if EnableStats.stats is None:
        EnableStats.stats = dict()
    EnableStats.stats[function.__name__] = dict(
        module=function.__module__,
        nb_call=0,
        total_time=0,
        max_time = float('-inf'),
        min_time = float('inf'),
    )

    def decorator(*args, **kwargs):
        if not EnableStats.enable:
            return function(*args, **kwargs)
        EnableStats.stats[function.__name__]['nb_call'] += 1
        time_start = time.time()
        ret = function(*args, **kwargs)
        exec_time = time.time() - time_start
        EnableStats.stats[function.__name__]['total_time'] += exec_time
        EnableStats.stats[function.__name__]['max_time'] = max(EnableStats.stats[function.__name__]['max_time'], exec_time)
        EnableStats.stats[function.__name__]['min_time'] = min(EnableStats.stats[function.__name__]['min_time'], exec_time)
        return ret
    return decorator


def get_and_print_stats(compact=True, pr_nb_called=True, pr_total_exec_time=True, pr_mean_time=True, pr_frequency=1):
    """
    this decorator get stats about one function and print it
    :param compact: print in compact format (only one line) -> default False
    :param pr_nb_called: print the number of call of the function -> default True
    :param pr_total_exec_time: print the total time of exec on this function -> default True
    :param pr_mean_time: print the mean exec time of this function
    :param pr_frequency: the frequency to print the stats (for example if pr_frequency is 10, the function print the result every 10 call)
    """
    def print_stats_in_exec(function):
        if EnableStats.stats is None:
            EnableStats.stats = dict()
        EnableStats.stats[function.__name__] = dict(
            module=function.__module__,
            nb_call=0,
            total_time=0,
            max_time = float('-inf'),
            min_time = float('inf'),
        )

        def decorator(*args, **kwargs):
            if not EnableStats.enable:
                return function(*args, **kwargs)
            EnableStats.stats[function.__name__]['nb_call'] += 1
            time_start = time.time()
            ret = function(*args, **kwargs)
            exec_time = time.time() - time_start
            EnableStats.stats[function.__name__]['total_time'] += exec_time
            EnableStats.stats[function.__name__]['max_time'] = max(EnableStats.stats[function.__name__]['max_time'], exec_time)
            EnableStats.stats[function.__name__]['min_time'] = min(EnableStats.stats[function.__name__]['min_time'], exec_time)
            if EnableStats.stats[function.__name__]['nb_call'] % pr_frequency == 0 or \
               EnableStats.stats[function.__name__]['nb_call'] == 1:
                print_stats_one_function(function.__name__,
                        compact=compact,
                        pr_nb_called=pr_nb_called,
                        pr_total_exec_time=pr_total_exec_time,
                        pr_mean_time=pr_mean_time,)
            return ret
        return decorator
    return print_stats_in_exec

def print_stats_one_function(name, compact=False, pr_nb_called=True, pr_total_exec_time=True, pr_mean_time=True):
    """
    print stats about one function
    :param name: the function name
    :param compact: print in compact format (only one line) -> default False
    :param pr_nb_called: print the number of call of the function -> default True
    :param pr_total_exec_time: print the total time of exec on this function -> default True
    :param pr_mean_time: print the mean exec time of this function
    """
    val = EnableStats.stats[name]
    if compact:
        s = '%s.py -> %s(' % (val['module'], name)
        if pr_nb_called:
            s += 'called %d times' % (val['nb_call'])
        if val['nb_call'] > 0:
            if pr_total_exec_time:
                s += ' total: %fs' % (val['total_time'])
            if pr_mean_time:
                s += ' average: %fs' % (val['total_time'] / val['nb_call'])
        s += ')'
        print(s)
    else:
        print('%s.py -> %s():' % (val['module'], name))
        if pr_nb_called:
            print('\tfunction called %d times' % (val['nb_call']))
        if val['nb_call'] > 0:
            if pr_total_exec_time:
                print('\ttotal exec time %fs' % (val['total_time']))
            if pr_mean_time:
                print('\tmean time %fs (min: %fs, max: %fs)' % (val['total_time'] / val['nb_call'], val['min_time'], val['max_time']))


def print_stats(compact=False, pr_nb_called=True, pr_total_exec_time=True, pr_mean_time=True):
    """
    print stats about one or all functions
    :param compact: print in compact format (only one line) -> default False
    :param pr_nb_called: print the number of call of the function -> default True
    :param pr_total_exec_time: print the total time of exec on this function -> default True
    :param pr_mean_time: print the mean exec time of this function
    """

    if EnableStats.stats is None or not EnableStats.enable:
        return
    for key in EnableStats.stats:
        print_stats_one_function(key,
                                 compact=compact,
                                 pr_nb_called=pr_nb_called,
                                 pr_total_exec_time=pr_total_exec_time,
                                 pr_mean_time=pr_mean_time,)
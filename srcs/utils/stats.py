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
    markers = {}

def _set_marker_def_val(func_name, marker_name):
    EnableStats.stats[func_name]['marker'][marker_name] = dict(
        module=EnableStats.stats[func_name]['module'],
        nb_call=0,
        total_time=0,
        max_time = float('-inf'),
        min_time = float('inf'),
        print_=True,
        pr_nb_call=True,
        pr_mean_time=True,
        pr_total_time=True,
        pr_min_time=True,
        pr_max_time=True,
    )

def _reset_marker_values(func_name, marker_name):
    EnableStats.stats[func_name]['marker'][marker_name]["module"] = EnableStats.stats[func_name]['module']
    EnableStats.stats[func_name]['marker'][marker_name]["nb_call"] = 0
    EnableStats.stats[func_name]['marker'][marker_name]["total_time"] = 0
    EnableStats.stats[func_name]['marker'][marker_name]["max_time"] = float('-inf')
    EnableStats.stats[func_name]['marker'][marker_name]["min_time"] = float('inf')

def _set_function_def_val(function):
    if EnableStats.stats is None:
        EnableStats.stats = dict()
    EnableStats.stats[function.__name__] = dict(
        module=function.__module__,
        nb_call=0,
        total_time=0,
        max_time = float('-inf'),
        min_time = float('inf'),
        marker = {},
        pr_nb_call=True,
        pr_mean_time=True,
        pr_total_time=True,
        pr_min_time=True,
        pr_max_time=True,
    )

def _stats_one_func(function, *args, **kwargs):
    EnableStats.stats[function.__name__]['nb_call'] += 1
    time_start = time.time()
    ret = function(*args, **kwargs)
    exec_time = time.time() - time_start
    EnableStats.stats[function.__name__]['total_time'] += exec_time
    EnableStats.stats[function.__name__]['max_time'] = max(EnableStats.stats[function.__name__]['max_time'], exec_time)
    EnableStats.stats[function.__name__]['min_time'] = min(EnableStats.stats[function.__name__]['min_time'], exec_time)
    for mark in EnableStats.stats[function.__name__]['marker']:
        EnableStats.stats[function.__name__]['marker'][mark]['nb_call'] += 1
        EnableStats.stats[function.__name__]['marker'][mark]['total_time'] += exec_time
        EnableStats.stats[function.__name__]['marker'][mark]['max_time'] = max(EnableStats.stats[function.__name__]['marker'][mark]['max_time'], exec_time)
        EnableStats.stats[function.__name__]['marker'][mark]['min_time'] = min(EnableStats.stats[function.__name__]['marker'][mark]['min_time'], exec_time)
    return ret

def get_stats(function):
    """
    this decorator get stats about one function
    """
    _set_function_def_val(function)

    def decorator(*args, **kwargs):
        if not EnableStats.enable:
            return function(*args, **kwargs)
        ret = _stats_one_func(function, *args, **kwargs)
        return ret
    return decorator

def get_and_print_stats(compact=True, pr_nb_call=True, pr_total_time=True, pr_mean_time=True, pr_frequency=1):
    """
    this decorator get stats about one function and print it
    :param compact: print in compact format (only one line) -> default False
    :param pr_nb_called: print the number of call of the function -> default True
    :param pr_total_exec_time: print the total time of exec on this function -> default True
    :param pr_mean_time: print the mean exec time of this function
    :param pr_frequency: the frequency to print the stats (for example if pr_frequency is 10, the function print the result every 10 call)
    """
    def print_stats_in_exec(function):
        _set_function_def_val(function)

        def decorator(*args, **kwargs):
            if not EnableStats.enable:
                return function(*args, **kwargs)
            ret = _stats_one_func(function, *args, **kwargs)
            if EnableStats.stats[function.__name__]['nb_call'] % pr_frequency == 0 or \
               EnableStats.stats[function.__name__]['nb_call'] == 1:
                print_stats_one_function(function.__name__, EnableStats.stats[function.__name__],
                        compact=compact,
                        pr_nb_call=pr_nb_call,
                        pr_total_time=pr_total_time,
                        pr_mean_time=pr_mean_time,)
            return ret
        return decorator
    return print_stats_in_exec

def get_stats_and_mark(name="default_marker", print_=True, pr_nb_call=True, pr_total_time=True, pr_mean_time=True, pr_min_time=True, pr_max_time=True):
    """
    mark this function -> the function will have a marker and get stats from this marker
    """
    def marker(function):
        _set_function_def_val(function)
        _set_marker_def_val(func_name=function.__name__, marker_name=name)
        if name not in EnableStats.markers:
            EnableStats.markers[name] = []  # functions name list
        EnableStats.markers[name].append(function.__name__)
        EnableStats.stats[function.__name__]['marker'][name]['print_'] = print_
        if not pr_nb_call:
            EnableStats.stats[function.__name__]['marker'][name]['pr_nb_call'] = False
        if not pr_total_time:
            EnableStats.stats[function.__name__]['marker'][name]['pr_total_time'] = False
        if not pr_mean_time:
            EnableStats.stats[function.__name__]['marker'][name]['pr_mean_time'] = False
        if not pr_min_time:
            EnableStats.stats[function.__name__]['marker'][name]['pr_min_time'] = False
        if not pr_max_time:
            EnableStats.stats[function.__name__]['marker'][name]['pr_max_time'] = False

        def decorator(*args, **kwargs):
            if not EnableStats.enable:
                return function(*args, **kwargs)
            ret = _stats_one_func(function, *args, **kwargs)
            return ret
        return decorator
    return marker


def set_marker(name="default_marker", beforetxt="", aftertxt="\n"):
    """
    create a marker with the name 'name'
    foreach call of reset_marker -> calc new parallele stats
    """
    def marker(function):
        if name not in EnableStats.markers:
            EnableStats.markers[name] = []  # functions name list
        def decorator(*args, **kwargs):
            if not EnableStats.enable:
                return function(*args, **kwargs)
            print(end=beforetxt)
            ret = function(*args, **kwargs)
            for func_name in EnableStats.markers[name]:
                if EnableStats.stats[func_name]['marker'][name]['print_']:
                    print_stats_marker_one_function(name=func_name, marker_name=name)
                _reset_marker_values(func_name=func_name, marker_name=name)
            print(end=aftertxt)
            return ret
        return decorator
    return marker

def print_stats_marker_one_function(name, marker_name="default_marker"):
    print_stats_one_function(name, EnableStats.stats[name]['marker'][marker_name], compact=True)

def print_stats_one_function(name, val, compact=False, pr_nb_call=True, pr_total_time=True, pr_mean_time=True, pr_min_time=True, pr_max_time=True):
    """
    print stats about one function
    :param name: the function name
    :param compact: print in compact format (only one line) -> default False
    :param pr_nb_called: print the number of call of the function -> default True
    :param pr_total_exec_time: print the total time of exec on this function -> default True
    :param pr_mean_time: print the mean exec time of this function
    """
    if compact:
        s = '%s.py -> %s(' % (val['module'], name)
        if pr_nb_call and val['pr_nb_call']:
            s += 'called %d times ' % (val['nb_call'])
        if val['nb_call'] > 0:
            if pr_total_time and val['pr_total_time']:
                s += 'total: %fs ' % (val['total_time'])
            if val['nb_call'] > 1:
                if pr_mean_time and val['pr_mean_time']:
                    s += 'average: %fs ' % (val['total_time'] / val['nb_call'])
                if pr_min_time and val['pr_min_time']:
                    s += 'min: %fs ' % (val['min_time'])
                if pr_max_time and val['pr_max_time']:
                    s += 'max: %fs ' % (val['max_time'])
        s = s.strip() + ')'
    else:
        s = '%s.py -> %s():\n' % (val['module'], name)
        if pr_nb_call and val['pr_nb_call']:
            s += '\tfunction called %d times\n' % (val['nb_call'])
        if val['nb_call'] > 0:
            if pr_total_time and val['pr_total_time']:
                s += '\ttotal exec time %fs\n' % (val['total_time'])
            if val['nb_call'] > 1:
                if pr_mean_time and val['pr_mean_time']:
                    s += '\taverage: %fs\n' % (val['total_time'] / val['nb_call'])
                if pr_min_time and val['pr_min_time']:
                    s += '\tmin: %fs\n' % (val['min_time'])
                if pr_max_time and val['pr_max_time']:
                    s += '\tmax: %fs' % (val['max_time'])
    print(s)

def print_stats(compact=False, pr_nb_call=True, pr_total_time=True, pr_mean_time=True, pr_min_time=True, pr_max_time=True):
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
        print_stats_one_function(key, EnableStats.stats[key],
                                 compact=compact,
                                 pr_nb_call=pr_nb_call,
                                 pr_total_time=pr_total_time,
                                 pr_mean_time=pr_mean_time,
                                 pr_min_time=pr_min_time,
                                 pr_max_time=pr_max_time,
                                 )

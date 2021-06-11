import re
import time
import logging
from functools import wraps

import networkx as nx
import matplotlib.pyplot as plt


pyqlog = logging.Logger()
Qubit = None


def statistics_time(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        data = args[0]
        if isinstance(data, dict):
            qubit = data.get('qubit')
            bit_info = qubit.bit
            node_dict = data.get('node_dict')
            node = node_dict.get(func.__name__)
        else:
            bit_info = 'all'
            node = func.__name__
        pyqlog.info(
            f'\n\n*********************Qubit {bit_info} execute {node} start...\n')
        ret = func(*args, **kwargs)
        diff = time.time() - start
        pyqlog.info(f'\n\n*********************Qubit {bit_info} execute {node} end. '
                    f'Consume time: {diff} s.\n')
        return ret

    return inner


def whether_import_save(func):
    @wraps(func)
    def inner(*args, is_import=True, is_save=True, **kwargs):
        qubit = None
        if is_import is True:
            for variate in args:
                if isinstance(variate, Qubit):
                    qubit = variate
                    break
            qubit.import_qubit()

        ret = func(*args, **kwargs)
        if is_save is True:
            for variate in args:
                if isinstance(variate, Qubit):
                    qubit = variate
                    break
            qubit.save_qubit()
        return ret

    return inner


def list_to_dict(node_list: list):
    """
    Convert the list to a dictionary,
    Create a dictionary, key is a element in the list,
    value is a element which next the key, if no exists, the value is None.
    Args:
        node_list (list): normal, list of node

    Returns:
        schema (dict): a dictionary
    """
    length = len(node_list)
    if length == 0:
        schema = {}
    elif length == 1:
        schema = {node_list[0]: None}
    else:
        new_node_list = node_list[1:]
        new_node_list.append(None)
        schema = {k: v for k, v in zip(node_list, new_node_list)}

    return schema


def make_graph(schema):
    """ Construct the task graph (dag) from a given schema.

    Parses the graph schema definition and creates the task graph. Tasks are the
    vertices of the graph and the connections defined in the schema become the edges.

    A key in the schema dict represents a parent task and the value one or more
    children:
        {parent: [child]} or {parent: [child1, child2]}

    The data output of one task can be routed to a labelled input slot of successor
    tasks using a dictionary instead of a list for the children:
        {parent: {child1: 'positive', child2: 'negative'}}

    An empty slot name or None skips the creation of a labelled slot:
        {parent: {child1: '', child2: None}}

    The underlying graph library creates nodes automatically, when an edge between
    non-existing nodes is created.

    Args:
        schema (dict): A dictionary with the schema definition.

    Returns:
        DiGraph: A reference to the fully constructed graph object.

    Raises:
        DirectedAcyclicGraphUndefined: If the schema is not defined.
    """

    # sanitize the input schema such that it follows the structure:
    #    {parent: {child_1: slot_1, child_2: slot_2, ...}, ...}
    sanitized_schema = {}
    for parent, children in schema.items():
        child_dict = {}
        if children is not None:
            if isinstance(children, list):
                if len(children) > 0:
                    child_dict = {child: None for child in children}
                else:
                    child_dict = {None: None}
            elif isinstance(children, dict):
                for child, slot in children.items():
                    child_dict[child] = slot if slot != '' else None
            else:
                child_dict = {children: None}
        else:
            child_dict = {None: None}

        sanitized_schema[parent] = child_dict

    # build the graph from the sanitized schema
    graph = nx.DiGraph()
    for parent, children in sanitized_schema.items():
        for child, slot in children.items():
            if child is not None:
                graph.add_edge(parent, child, slot=slot)
            else:
                graph.add_node(parent)

    return graph


def plot_dag(dag, png_name):
    fig, axs = plt.subplots(figsize=(36, 12))
    labels = {k: '\n'.join(k.split('_')[:-1])
              for k in nx.topological_sort(dag)}
    pos = {k: [i + 1, 6] for i, k in enumerate(nx.topological_sort(dag))}
    nx.draw(dag,
            pos=pos,
            with_labels=True,
            labels=labels,
            node_shape='o',  # one of 'so^>v<dph8'
            node_size=13000,
            font_size=18)
    # plt.show()
    fig.savefig(png_name)
    plt.close(fig)


def some():
    pattern = re.compile(r'^q(\d)_.*?yaml$')
    yaml_path = r'D:\ssfang\data\qubit_info'
    file_list = os.listdir(yaml_path)
    for file in file_list:
        print(file)
        file_path = f'{yaml_path}/{file}'
        bit = pattern.match(file).group(1)
        qubit = Qubit(bit)
        qubit.save_by_yaml(file_path)


def get_z_amp():
    # get z_amp
    z_amp_list = []
    diff_list = [60, 120, 180, 300, 300]
    for diff in diff_list:
        diff_freq = qubit.drive_freq - diff
        z_amp = freq2amp_formula(diff_freq, *ac_spectrum_params)
        z_amp_list.append(z_amp)

    new_repeat_loops = np.array(repeat_loops)
    new_repeat_loops[:, 1] = np.array(z_amp_list)
    pyqlog.debug(f'Qubit {qubit.bit} z_amp_list: {z_amp_list}')
    pyqlog.debug(f'repeat_loops: {repeat_loops}')
    pyqlog.debug(f'new_repeat_loops: \n{new_repeat_loops}')

#!/usr/bin/env python
from mpi4py import MPI
import sys
import numpy as np
import inspect

def initialize_mpi(debug=False):

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    name = MPI.Get_processor_name()

    
    if (debug):
        print "Process Rank= ", rank
        print "Size= ", size

    return rank, size, comm

def wait_for_message(recv_buff, status, comm, debug=False):
    
    comm.Recv(recv_buff, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
    source = status.Get_source()
    tag    = status.Get_tag()

    return recv_buff, source, tag
def get_chunk(all_data, current_index, chunk_size):

    ci = current_index
    pi = min(chunk_size, len(all_data[ci:]))
    chunk = all_data[ci:ci+pi]
    new_index = ci+pi
    return chunk, new_index

def send_data(data_chunk, destination, comm, tag=0):
    comm.send(data_chunk, dest=destination, tag=tag)
    return

def process_data(local_data, pre, fancy=''):
    for thing in local_data:
        print pre, fancy, thing
    return

def needs_current_index_arg(function):
    #See https://stackoverflow.com/questions/196960/
    #    can-you-list-the-keyword-arguments-a-function-receives 
    args, varargs, varkw, defaults = inspect.getargspec(function)
    return ('current_index' in args)

def perform_task_in_parallel(function, args, kwargs, all_data,
                             chunk_size, rank, size, comm,
                             root=0, debug=False):
    """
    Perform a function on all_data in parallel. 
    The set all_data is broken into chunks on the 
    root processor and passed to worker processors 
    whenever the are marked as idle. 
    This ensures all processors are always busy 
    (as opposed to equally partitioning all_data to 
    each proc as parallelization does).

    Function takes args and kwargs in the form 
    function(local_data, *args, **kwargs) 
    where local_data is the chunk sent by the root, 
    args are the passed arguments, 
    and **kwargs is a dictionary of {'kw':'arg'} 
    to be unrolled to kw=arg once the function is called.
    """
    pre = "Proc", rank
    status = MPI.Status()

    send_me_work = np.array([999], dtype=int)
    everyone_all_done = np.array([100], dtype=int)
    recv_buff  = np.zeros(1, dtype=int)
    work_tag = 999
    done_tag = 100
    
    # For keeping track of who's
    # currently doing what, we use an integer
    # array called procs_status.
    idle    = 200
    working = 999
    done    = 100

    # Everyone starts idle.
    procs_status = np.zeros(size-1)
    procs_status[:] = idle

    not_done = True
    current_index = 0

    counter = 0
    frac_done = 0.

    comm.Barrier()

    if (rank == root):
        number_of_work_units = len(all_data)
        last_data_index = len(all_data)-1
        procs_status[:] = working

    if (rank == root): #Supervisor processor
        while (np.array(procs_status != done).any()):

            if ( int((float(counter)
                      / float(number_of_work_units)
                      / float(chunk_size))*100.) >= frac_done ):
                print "Progress at {:.0f} %".format(frac_done)
                frac_done += 3

            recv_buff, source, tag = wait_for_message(recv_buff, status,
                                                      comm, debug=debug)
            if (not_done):

                data_chunk, new_index = get_chunk(all_data,
                                                  current_index, chunk_size)
            if (recv_buff == send_me_work and not_done):
                comm.Send([send_me_work, 1, MPI.INT],
                          dest=source, tag=current_index)
                
                send_data(data_chunk, source, comm, tag=current_index)
                procs_status[source-1] = working
            else:
                comm.Send([everyone_all_done, MPI.INT],
                          dest=source, tag=done_tag)
                procs_status[source-1] = done

            current_index = new_index
            if (current_index > last_data_index):
                not_done = False

            counter += 1

    else:

        while not_done:

            comm.Send([send_me_work, 1, MPI.INT], dest=root, tag=0)

            comm.Recv([recv_buff, MPI.INT],
                      source=root, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()

            if (recv_buff != done_tag):
                local_data = comm.recv(source=root, tag=tag, status=status)
                if (needs_current_index_arg(function)):
                    kwargs['current_index']=tag
                function(local_data, *args, **kwargs)
            else:
                if (recv_buff == everyone_all_done):
                    not_done = False
    print pre, "Exiting from perform_task_in_parallel"
    return
                
def test_mpi_task(debug):
    rank, size, comm = initialize_mpi(debug=debug)

    root = 0
    all_data = None
    chunk_size = None

    if (rank == root):
        all_data = np.arange(10)
        chunk_size = 1
    pre = "Proc", rank
    args = [pre]
    kwargs = {'fancy':'very fancy'}

    perform_task_in_parallel(process_data, args, kwargs,
                             all_data, chunk_size, rank, size,
                             comm, debug=debug)
    print "We're all done here"

if (__name__ == '__main__'):
    debug = True
    test_mpi_task(debug)

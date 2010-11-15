import time, cPickle as pickle

POLL_INTERVAL = 0.5 # seconds

class Master(object):
    def __init__(self, nodes):
        self.nodes = nodes

    def run(self, job):
        """Distributes data to nodes and then runs `job` on all nodes. Returns
        the sum of the nodes' responses."""
        self.__distribute_data(job.name, job.dataset)

        # run tasks
        for i,node in enumerate(self.nodes):
            task_name = self.__slice_name(job.name, i)
            node.run_task(job, task_name)

        # poll for and reduce task outputs
        result = 0
        polled = False
        for i,node in enumerate(self.nodes):
            task_name = self.__slice_name(job.name, i)
            while not node.task_is_finished(task_name):
                time.sleep(POLL_INTERVAL)
                if polled:
                    print "poll for %s, try again in %.1f sec" % \
                        (task_name, POLL_INTERVAL)
                else:
                    polled = True # print msg next time
            task_output = node.task_output(task_name)
            result += pickle.loads(task_output)
        
        return result

    def __slice_name(self, job_name, slice_num):
        return "%s_slice%dof%d" % (job_name, slice_num, len(self.nodes))

    def __distribute_data(self, job_name, dataset):
        for i,node in enumerate(self.nodes):
            slice = dataset.slice(len(self.nodes), i)
            slice_name = self.__slice_name(job_name, i)
            if slice_name not in node.slices.list():
                node.slices.put(slice_name, pickle.dumps(slice))
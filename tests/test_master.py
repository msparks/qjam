from nose.tools import *

import numpy

from qjam.dataset import DataSet
from qjam.master.master import Master
from qjam.master.remote_worker import RemoteWorker

# Test modules.
from modules import constant
from modules import inner_prod
from modules import multiply_sum_simple
from modules import sum_params
from modules import write_to_stdout


class TestMaster:
  def test_single_worker_simple(self):
    worker = RemoteWorker('localhost')
    master = Master([worker])

    assert_equals(42, master.run(constant))

    params = [1, 2, 3, 6, 7, 9]
    assert_equals(sum(params), master.run(sum_params, params))

  def test_dual_worker_simple(self):
    worker_1 = RemoteWorker('localhost')
    worker_2 = RemoteWorker('localhost')
    master = Master([worker_1, worker_2])

    assert_equals(84, master.run(constant))

    params = [1, 2, 3, 6, 7, 9]
    assert_equals(2 * sum(params), master.run(sum_params, params))

  def test_single_worker_multiply_sum_simple(self):
    worker = RemoteWorker('localhost')
    master = Master([worker])

    dataset = DataSet(range(0,100))
    result = master.run(multiply_sum_simple, params=3, dataset=dataset)

    assert_equals(14850, result)

  def test_triple_worker_multiply_sum_simple(self):
    worker_1 = RemoteWorker('localhost')
    worker_2 = RemoteWorker('localhost')
    worker_3 = RemoteWorker('localhost')
    master = Master([worker_1, worker_2, worker_3])

    dataset = DataSet(range(0,100))
    result = master.run(multiply_sum_simple, params=3, dataset=dataset)

    assert_equals(14850, result)

  def test_numpy(self):
    worker_1 = RemoteWorker('localhost')
    worker_2 = RemoteWorker('localhost')
    master = Master([worker_1, worker_2])

    dataset = DataSet(numpy.array([[1,2],[3,4],[5,6],[7,8],[9,10]]))
    params = numpy.array([2,4])
    result = master.run(inner_prod, params=params, dataset=dataset)

    assert_equals(170, result)

  def test_write_to_stdout(self):
    worker_1 = RemoteWorker('localhost')
    master = Master([worker_1])

    dataset = DataSet(range(0, 100))
    result = master.run(write_to_stdout, params=1, dataset=dataset)

    assert_equals(42, result)

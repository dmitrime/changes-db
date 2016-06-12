import sys
from pytest import fixture, raises
from datetime import datetime

sys.path.append('.')
sys.path.append('..')

from model import ChangesDB


def test_load(db):
    assert len(db.data) == 4

def test_load_empty():
    with raises(Exception) as e:
        ChangesDB('data/empty.csv')
    assert 'valid' in str(e.value)

def test_load_bad():
    with raises(Exception) as e:
        ChangesDB('data/bad.csv')
    assert 'dimentions' in str(e.value)

def test_keys(db):
    assert len(db.keys()) == 2
    assert db.keys() == ['ObjectA', 'ObjectB']

def test_query_empty(db):
    assert db.query(None, None, None) is None

def test_query_without_id(db):
    tp, ts = 'ObjectA', 467765765
    val = db.query(tp, None, ts)
    assert val is not None
    assert len(val) == 2
    assert val[0]['id'] == 1 and val[1]['id'] == 2
    assert val[0]['type'] == tp and val[1]['type'] == tp
    assert val[0]['time'] <= datetime.fromtimestamp(ts)
    assert val[1]['time'] <= datetime.fromtimestamp(ts)

def test_query_with_id(db):
    i, tp, ts = 1, 'ObjectA', 467765765
    val = db.query(tp, i, ts)
    assert val is not None
    assert len(val) == 1
    assert val[0]['id'] == i
    assert val[0]['type'] == tp
    assert val[0]['time'] <= datetime.fromtimestamp(ts)

def test_query_time_props(db):
    i, tp, ts = 1, 'ObjectA', 467765763
    val = db.query(tp, i, ts)
    assert val is not None
    assert len(val) == 1
    assert val[0]['id'] == i
    assert val[0]['type'] == tp
    assert val[0]['time'] <= datetime.fromtimestamp(ts)
    assert len(val[0]['props']) == 2
    assert val[0]['props']['property1'] == 'value1'

    ts = 467765765
    val = db.query(tp, i, ts)
    assert val is not None
    assert len(val) == 1
    assert val[0]['id'] == i
    assert val[0]['type'] == tp
    assert val[0]['time'] <= datetime.fromtimestamp(ts)
    assert len(val[0]['props']) == 3
    assert val[0]['props']['property1'] == 'altered value1'


@fixture
def db():
    return ChangesDB('data/sample.csv')

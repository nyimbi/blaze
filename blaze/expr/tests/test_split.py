from blaze.expr import *
from blaze.expr.split import *
import datashape

t = TableSymbol('t', '{name: string, amount: int, id: int}')


def test_path_split():
    expr = t.amount.sum() + 1
    assert path_split(t, expr).isidentical(t.amount.sum())

    expr = t.amount.distinct().sort()
    assert path_split(t, expr).isidentical(t.amount.distinct())

    t2 = t.distinct()
    expr = by(t2.id, amount=t2.amount.sum()).amount + 1
    assert path_split(t, expr).isidentical(by(t2.id, amount=t2.amount.sum()))



def test_sum():
    expr = t.amount.sum()
    a, b = split(t, expr)

    (chunk, chunk_expr), (agg, agg_expr) = split(t, t.amount.sum())

    assert chunk.schema == t.schema
    assert chunk_expr.isidentical(chunk.amount.sum())

    assert agg.iscolumn
    assert agg_expr.isidentical(sum(agg))

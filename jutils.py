def ladder(iterable, nocap=False, cap=None):
    it = iter(iterable)
    last = next(it) if nocap else cap 
    for i in it:
        yield (last, i)
        last = i
    if not nocap:
        yield (last, cap)


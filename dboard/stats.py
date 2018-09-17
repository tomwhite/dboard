def time_in_range(data, bg_range=(4.0, 7.0)):
    # data[0] is the time values - assume they are equally spaced, so we can ignore
    values = data[1]
    return 100.0 * sum([bg_range[0] <= v <= bg_range[1] for v in values]) / len(values)


def mean(data):
    values = data[1]
    return float(sum(values)) / len(values)


def estimated_hba1c(data):
    # from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2742903/
    return hba1c_ngsp_to_ifcc((mean(data) + 2.59) / 1.59)


def hba1c_ngsp_to_ifcc(ngsp):
    # from http://www.ngsp.org/ifccngsp.asp
    return 10.93 * ngsp - 23.50

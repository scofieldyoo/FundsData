import string
import os
from funds_gen_sorting_files import ALL_FUNDS
from settings import TODAY, RESULT_DIR


def _gen_set(order, Top):
    funds = []
    for rec in ALL_FUNDS:
        if rec[order].find('%') != -1:
            funds.append(rec)
    
    count = 0
    my_list = []
    for rec in sorted(funds, key=lambda record: string.atof(record[order].split("%")[0]), reverse=True):
        my_list.append('\t'.join([rec["Code"], rec["Title"]]))
        count += 1
        if count >= Top:
            break
    
    my_set = set(my_list)
    return my_set


def get_intersection(WriteFile, Top=100,
                     Inc3Years=True, Inc2Years=True, Inc1Year=True,
                     Inc6Months=True, Inc3Months=True, Inc1Month=True):
    
    set_3years = _gen_set("Inc3Years", Top) if Inc3Years else set()
    set_2years = _gen_set("Inc2Years", Top) if Inc2Years else set()
    set_1year = _gen_set("Inc1Year", Top) if Inc1Year else set()
    set_6months = _gen_set("Inc6Months", Top) if Inc6Months else set()
    set_3months = _gen_set("Inc3Months", Top) if Inc3Months else set()
    set_1month = _gen_set("Inc1Month", Top) if Inc1Month else set()
    
    final_set = set_3years if Inc3Years else None
    if Inc2Years:
        final_set = final_set & set_2years if final_set else set_2years
    if Inc1Year:
        final_set = final_set & set_1year if final_set else set_1year
    if Inc6Months:
        final_set = final_set & set_6months if final_set else set_6months
    if Inc3Months:
        final_set = final_set & set_3months if final_set else set_3months
    if Inc1Month:
        final_set = final_set & set_1month if final_set else set_1month
    
    with open(WriteFile, "w") as wf:
        for item in final_set:
            wf.write(item + '\n')


def main():
    cfg_100_all = {'Top': 100, 'Inc3Years': True, 'Inc2Years': True, 'Inc1Year': True, 'Inc6Months': True, 'Inc3Months': True, 'Inc1Month': True}
    cfg_50_all = {'Top': 50, 'Inc3Years': True, 'Inc2Years': True, 'Inc1Year': True, 'Inc6Months': True, 'Inc3Months': True, 'Inc1Month': True}
    
    get_intersection(os.path.join(RESULT_DIR, "all_100_%s.txt" % TODAY), **cfg_100_all)
    get_intersection(os.path.join(RESULT_DIR, "all_50_%s.txt" % TODAY), **cfg_50_all)


if __name__:
    main()

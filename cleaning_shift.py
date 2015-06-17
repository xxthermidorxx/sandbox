#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import datetime

DAY_OF_WEEK = {
    "Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3,
    "Fri": 4, "Sat": 5, "Sun": 6
}
CLEAN_ON_WHEN = "Wed"       # 掃除をする曜日
HOW_MANY = 2                # 掃除をする人数


def decide_who_to_choose(student_tuple, assigned_dict):
    num = len(student_tuple)
    ids_to_choose = []
    while True:
        idx = random.randint(0, num-1)
        # 既にその人が選ばれていないか
        if idx in ids_to_choose:
            continue
        # 一巡するまでに回ってきていないか
        if assigned_dict[idx] is False:
            ids_to_choose.append(idx)
            assigned_dict[idx] = True
        # 一巡すれば始めから
        count = 0
        for idx, is_assigned in assigned_dict.items():
            if is_assigned is True:
                count += 1
        if count == num:
            for idx in xrange(0, num):
                assigned_dict[idx] = False
        if len(ids_to_choose) == HOW_MANY:
            break
    return ids_to_choose


# 日付と掃除当番のリストを作成
def clean_shift(student_tuple, begin_date, end_date):
    begin_year, begin_month, begin_day = [int(i) for i in begin_date.split("/")]
    begin = datetime.date(begin_year, begin_month, begin_day)
    end_year, end_month, end_day = [int(i) for i in end_date.split("/")]
    end = datetime.date(end_year, end_month, end_day)

    assert begin.weekday() == DAY_OF_WEEK[CLEAN_ON_WHEN], \
        "begin_dateには掃除をする曜日の日付を入力してください"

    shift_list = []
    assigned_dict = { idx: False for idx, student in enumerate(student_tuple) }
    while begin <= end:
        ids_to_choose = decide_who_to_choose(student_tuple, assigned_dict)
        who_to_choose = [student_tuple[idx] for idx in ids_to_choose]
        day = str(begin.month) + "/"+str(begin.day)
        shift_list.append( (day, ", ".join(who_to_choose)) )
        begin += datetime.timedelta(days=7)
    return shift_list


# Usage: python cleaning_shift.py 2015/1/1 2015/3/3
if __name__ == '__main__':
    argvs = sys.argv
    begin_date = argvs[1]
    end_date = argvs[2]

    student = (u"Alice", u"Bob", u"Carlos", u"Eduardo", u"Mike")
    shift_list = clean_shift(student, begin_date, end_date)

    for pair in shift_list:
        print pair[0] + ": " + pair[1]

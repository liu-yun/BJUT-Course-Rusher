import re

import course
import userinfo
import cache
from xk import login, get_name, base_url, retry_post


def sel_course(session, course_name, course_number, viewstate, username, name):
    h_url = 'http://' + base_url + '/xf_xsqxxxk.aspx'
    h_params = {
        'xh': username,
        'xm': name.encode('gb18030'),
        'gnmkdm': 'N121101'
    }
    h_head = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    h_data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': viewstate,
        'ddl_kcxz': '',
        'ddl_ywyl': '',
        'ddl_kcgs': '',
        'ddl_xqbs': '1',
        'ddl_sksj': '',
        'TextBox1': course_name.encode('gb2312'),
        'Button1': '  提交  '.encode('gb2312'),
        'dpkcmcGrid:txtChoosePage': '1',
        'dpkcmcGrid:txtPageSize': '200',
        'kcmcGrid:_ctl' + str(course_number + 1) + ':xk': 'on'
    }
    r = retry_post(3, session, h_url, params=h_params, data=h_data, headers=h_head, timeout=2)
    p = re.compile(r"<script language=\'javascript\'>alert\(\'.+?\'\);</script>")
    rp = p.findall(r.text)
    if len(rp):
        return 'Failed, ' + rp[0][37:-12]
    else:
        return 'Successfully selected!'


if __name__ == '__main__':
    s = login(userinfo.usr, userinfo.pwd)
    name = get_name(s, userinfo.usr)
    print(userinfo.usr, name)
    todo_course = course.course
    count = 0
    while 1:
        count += 1
        print('-' * 12, 'Loop', count)
        for index, cur_course in enumerate(todo_course):
            print('Trying to get', cur_course[0], cur_course[1])
            result = sel_course(s, cur_course[0], cur_course[1], cache.viewstates[index], userinfo.usr, name)
            print(result)

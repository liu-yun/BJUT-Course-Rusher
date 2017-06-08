import re

import userinfo
import course
from xk import base_url, login, get_name, get_viewstate


def get_course_viewstate(session, course_name, viewstate, username, name):
    h_url = 'http://' + base_url + '/xf_xsqxxxk.aspx'
    h_params = {
        'xh': username,
        'xm': name.encode('gb2312'),
        'gnmkdm': 'N121113'
    }
    h_head = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # refresh viewstate
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
        'Button2': '确定'.encode('gb2312'),
        'dpkcmcGrid:txtChoosePage': '1',
        'dpkcmcGrid:txtPageSize': '200',
    }
    r = session.post(h_url, params=h_params, data=h_data, headers=h_head, timeout=2)
    p = re.compile(r'<input type=\"hidden\" name=\"__VIEWSTATE\" value=\".+?\" />')
    rp = p.findall(r.text)
    view = rp[0][47:-4]
    return view


if __name__ == '__main__':
    s = login(userinfo.usr, userinfo.pwd)
    name = get_name(s, userinfo.usr)
    print(userinfo.usr, name)
    viewstate = get_viewstate(s, userinfo.usr, name)
    todo_course = course.course
    with open('cache.py', 'w+') as f:
        f.write('viewstates = [\n')
        for cur_course in todo_course:
            print('Trying to get viewstate', cur_course[0], cur_course[1])
            result = get_course_viewstate(s, cur_course[0], viewstate, userinfo.usr, name)
            f.write(f'    \'{result}\',\n')
        f.write('    ]\n')

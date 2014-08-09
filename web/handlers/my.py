#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
# Created on 2014-08-08 21:06:02

from base import *

def my_status(task):
    if task['disabled']:
        return u'停止'
    if task['last_failed_count']:
        return u'已失败%d次，重试中...' % task['last_failed_count']
    if task['last_failed'] > task['last_success']:
        return u'失败'
    if task['success_count'] == 0 and task['failed_count'] == 0 and task['next']:
        return u'正在准备为您签到'
    return u'正常'

class MyHandler(BaseHandler):
    @tornado.web.addslash
    @tornado.web.authenticated
    def get(self):
        user = self.current_user
        tpls = self.db.tpl.list(user['id'], fields=('id', 'siteurl', 'sitename', 'disabled', 'lock', 'last_success', 'ctime', 'mtime'))

        tasks = []
        for task in self.db.task.list(user['id'], fields=('id', 'tplid', 'disabled', 'last_success', 'success_count', 'failed_count', 'last_failed', 'next', 'last_failed_count')):
            tpl = self.db.tpl.get(task['tplid'], fields=('sitename', ) )
            task['sitename'] = tpl and tpl['sitename'] or '未命名'
            tasks.append(task)
        self.render('my.html', tpls=tpls, tasks=tasks, my_status=my_status)

handlers = [
        ('/my/?', MyHandler),
        ]


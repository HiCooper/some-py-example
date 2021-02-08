# -*- coding: utf-8 -*-
# @File    : AnalysisException.py
# @Date    : 2020/10/27
# @Author  : HiCooper
# @Desc    : 分析异常-业务异常


class AnalysisException(RuntimeError):
    def __init__(self, message, sid=''):
        self.message = message
        self.sid = sid

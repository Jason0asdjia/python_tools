from __future__ import print_function
import sys
import re
"""
    自用控制台进度条
    设定两种格式
    [=================================       ] 67/80 ( 83%) 13 to go
    Progress: [==========                              ]  25%
"""


class _ProgressBar(object):

    DEFAULT = 'Progress: %(bar)s %(percent)3d%%'
    FULL = '%(bar)s %(current)d/%(total)d (%(percent)3d%%) >> %(remaining)d to go'

    # 使用sys.stderr 不用换行输出
    # sys.flush 立即刷新
    def __init__(self,
                 total,
                 width=40,
                 fmt=DEFAULT,
                 symbol='=',
                 output=sys.stderr):
        # if not
        assert len(symbol) == 1

        self.total = total
        self.width = width
        self.symbol = symbol
        self.output = output
        # 替换场宽参数，?P<name>取str字符串，\g<name>取本身所传入self.fmt % args
        # (?P<name>)命名group的各部分为name，\g<name>提取外面传入
        # 只将%(current)d此模式匹配出来替换成%(current)2d 2根据total长度判读
        self.fmt = re.sub(r'(?P<name>%\(.+?\))d',
                          r'\g<name>%dd' % len(str(total)), fmt)

        self.current = 0

    def __call__(self):
        percent = self.current / float(self.total)
        size = int(self.width * percent)
        remaining = self.total - self.current
        bar = '[' + self.symbol * size + ' ' * (self.width - size) + ']'

        args = {
            'total': self.total,
            'bar': bar,
            'current': self.current,
            'percent': percent * 100,
            'remaining': remaining
        }
        print('\r' + self.fmt % args, file=self.output, end='')

    def done(self):
        self.current = self.total
        self()
        print('', file=self.output)


"""
from time import sleep

progress = ProgressBar(80, fmt=ProgressBar.FULL)

for x in range(progress.total):
    progress.current += 1
    progress()
    sleep(0.1)
progress.done()
"""

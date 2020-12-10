# -*- coding: utf-8 -*-
# @File    : main.py
# @Date    : 2020/10/26
# @Author  : HiCooper
# @Desc    : 消息队列服务 使用示例
import random
import sys

from rabbitmq.analysis_exception import AnalysisException
from rabbitmq.rabbitmq_service import QueueConfig
from rabbitmq.rabbitmq_service import RabbitMqService

queue_config = QueueConfig(binding_keys='coffee.superman')

# 实例化服务
rabbitmq_service = RabbitMqService(host='192.168.33.10', username='admin', password='1qaz@WSX',
                                   queue_config=queue_config)


def do_task(msg_body):
    print('do task: msg: %s' % msg_body)
    rabbitmq_service.update_status('1')
    randint = random.randint(0, 9)
    if randint % 2 == 0:
        raise AnalysisException('omg! how bad u are!')


if __name__ == '__main__':
    try:
        rabbitmq_service.start_listening(do_task)
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)

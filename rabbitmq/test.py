# -*- coding: utf-8 -*-
# @File    : main.py
# @Date    : 2020/10/26
# @Author  : HiCooper
# @Desc    : 消息队列服务 使用示例
import json
import random
import sys

from rabbitmq.analysis_exception import AnalysisException
from rabbitmq.rabbitmq_service import QueueConfig
from rabbitmq.rabbitmq_service import RabbitMqService

from logger_init import logger

queue_config = QueueConfig(binding_keys='coffee.superman')

# 实例化服务
rabbitmq_service = RabbitMqService(host='47.101.42.169', username='admin', password='okmnji123',
                                   queue_config=queue_config)


def do_task(record):
    if 'record_id' not in record:
        raise AnalysisException(message='illegal msg, miss:record_id')
    record_id = record['record_id']
    logger.debug('record_id: {}', record_id)
    rabbitmq_service.update_status(record_id, 'ON_CLASSIFY')
    randint = random.randint(0, 9)
    if randint % 2 == 0:
        raise AnalysisException(message='omg! how bad u are!')


if __name__ == '__main__':
    try:
        rabbitmq_service.start_listening(do_task)
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)

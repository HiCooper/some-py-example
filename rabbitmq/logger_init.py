# coding: utf-8

#  logger_init
#  @author HiCooper
#  @version 1.0
#  @date 2021/2/8 15:59

import logging

logging.basicConfig(filename='rabbitmq.log', level=logging.INFO)
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)
# -*- coding: utf-8 -*-
# @File    : rabbitmq_service.py
# @Date    : 2020/10/26
# @Author  : HiCooper
# @Desc    : 消息队列服务

import pika
from pika.credentials import PlainCredentials

import validators
from rabbitmq.analysis_exception import AnalysisException

import logging

logging.basicConfig(filename='rabbitmq.log', level=logging.INFO)
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class QueueConfig:
    def __init__(self, exchange=None, default_listen_queue='coffeeBabyQueue',
                 binding_keys='coffee.#'):
        """
        初始化队列相关配置
        :param str exchange: 交换机名称
        :param str default_listen_queue: 默认监听队列名称
        :param str binding_keys:  绑定路由key列表，多个用空格隔开, 默认 coffee.#
        """
        if exchange is None:
            raise ValueError('exchange can not be blank!')
        self.exchange = exchange
        self.default_listen_queue = default_listen_queue
        self.binding_keys = binding_keys.split()


class RabbitMqService:
    """
    rabbitmq 服务
    提供 消息发送服务和消息监听服务
    消息发送 路由模式为：mustang.#
    消息接收 路由模式为：coffee.#, 支持自定义模式后缀，对于自定义的模式，会自动创建关联队列（非持久排他队列, 队列仅当前连接可访问，连接断开自动删除，会话级）
    同时监听，默认担保队列：coffeeBabyQueue(持久化队列)
    """

    SEND_ROUTING_KEY_PREFIX = 'mustang.'

    def __init__(self, host, port=5672, username=None, password=None, queue_config=None):
        """
        初始化消息服务，建立连接，创建队列
        :param str host: IP
        :param int port: 端口
        :param str username: 用户名
        :param str password: 密码
        :param QueueConfig queue_config: 队列配置
        """
        if queue_config is None:
            raise ValueError('queue_config must supply!')
        #  establish a connection with RabbitMQ server
        credentials = ''
        if username is not None and password is not None:
            credentials = PlainCredentials(username=username, password=password)
        logger.info('connecting to rabbitmq server...')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, credentials=credentials))
        self.channel = connection.channel()
        self.exchange = queue_config.exchange
        self.default_listen_queue = queue_config.default_listen_queue
        self.binding_keys = queue_config.binding_keys
        for binding_key in self.binding_keys:
            queue_name = binding_key + '_Queue'
            self.channel.queue_declare(queue=queue_name, exclusive=True)
            self.channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=binding_key)

    def _send_message(self, message, msg_type='pass'):
        """
        投递消息到 模式为：mustang.# 的队列 => mustang.[msg_type]
        其中 模式： mustang.# 与 Java 约定，不可修改
        :param str message:  消息内容 str
        :param str msg_type: pass | fail 分别对应发送到成功和失败队列, 默认 pass
        :return:
        """
        # send message to queue(hello)
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.SEND_ROUTING_KEY_PREFIX + msg_type,
                                   body=message)
        logger.info("send %s message successful!", msg_type)

    def start_listening(self, do_task):
        """
        开始监听队列 default_listen_queue => 路由 binding_keys
        Java 会将消息 发送至模式 coffee.#
        @:param fun do_task 接收到消息后的处理函数
        callback(channel, method, properties, body)
                channel: BlockingChannel
                method: spec.Basic.Deliver
                properties: spec.BasicProperties
                body: bytes
        :return:
        """

        validators.require_callback(do_task, callback_name='do_task')

        def callback(ch, method, properties, body):
            delivery_tag = method.delivery_tag
            routing_key = method.routing_key
            logger.info("Received message from %s, body: %s ", (routing_key, body.decode('utf-8')))
            # 执行回调
            try:
                do_task()
                self._send_message('wow i received a message from you , i got u(%s)' % routing_key)
                self.channel.basic_ack(delivery_tag=delivery_tag)
            except AnalysisException as e:
                logger.info('analysis exception: error: %s', e.message)
                self._send_message(e.message, msg_type='fail')
                self.channel.basic_ack(delivery_tag=delivery_tag)
            except BaseException as e:
                logger.info('something bad happened..., message will requeue, error: %s', e.args)
                self.channel.basic_reject(delivery_tag=delivery_tag)
            finally:
                logger.info('Done !')

        for binding_key in self.binding_keys:
            queue_name = binding_key + '_Queue'
            # bind exchange
            self.channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=binding_key)
            # set consume info
            self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
        # handle guarantee queue
        self.channel.basic_consume(queue=self.default_listen_queue, on_message_callback=callback, auto_ack=False)

        logger.info('Start listening message with binding routing_keys: %s', self.binding_keys)
        self.channel.start_consuming()

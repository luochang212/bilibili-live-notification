# -*- coding: utf-8 -*-

"""Notification for live
    Author: github@luochang212
    Date: 2021-08-11
    Usage: 
        (open cron and input)
        */3 * * * * source ~/.bash_profile; cd [PATH_TO_YOUR_SCRIPT]; python alert.py >> ../log/alert.log 2>> ../log/alert.err
"""


import subprocess
import configparser
import requests
import json
import logging


CONFIG_PATH = '../conf/live.conf'
SIGNAL_PATH = '../conf/signal.conf'
LOG_PATH = '../log/alert_info.log'


class Alert:
    """an alert"""

    def __init__(self, config_path: str = CONFIG_PATH, signal_path: str = SIGNAL_PATH, log_path: str = LOG_PATH):
        """init"""
        self.signal_path = signal_path
        self.config = self.get_config(config_path)
        self.logger = self.create_logger(log_path)

    @staticmethod
    def create_logger(log_path: str, logger_name: str = 'main.logger'):
        """create logger"""
        # create logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # create file handler and set level to debug
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s\t%(message)s')
        file_handler.setFormatter(formatter)  # add formatter to file_handler

        # add file_handler to logger
        logger.addHandler(file_handler)

        return logger

    @staticmethod
    def get_config(filename: str):
        config = configparser.ConfigParser()
        config.read(filename)
        return config

    def get_signal(self):
        signal_config = self.get_config(self.signal_path)
        previous_status = signal_config.get('signal', 'previous_status')

        return int(previous_status)

    def set_signal(self, status: int):
        """set signal variable"""
        signal_config = configparser.ConfigParser()
        signal_config['signal'] = {}
        signal_config['signal']['previous_status'] = str(status)
        with open(self.signal_path, 'w') as f:
            signal_config.write(f)

    def api_parser(self):
        """api parser"""
        api_url = self.config.get('live_info', 'api_url')
        live_room = self.config.get('live_info', 'live_room')
        url = api_url + live_room
        r = requests.get(url)

        live_info = json.loads(r.text)
        live_status = live_info.get('data', {}).get(
            'room_info', {}).get('live_status', '')

        if isinstance(live_status, int):
            return live_status

        return -1

    def send_notification(self, title: str, content: str):
        cmd = f'display notification "{content}" with title "{title}"'
        subprocess.call(["osascript", "-e", cmd])

    def controller(self):
        """main function"""
        live_status = self.api_parser()
        print(f'live_status: {live_status}')

        # get previous signal
        previous_signal = self.get_signal()

        # overwrite previous signal
        self.set_signal(live_status)

        if live_status == 1 and live_status != previous_signal:
            title = self.config.get('notification', 'title')
            content = self.config.get('notification', 'content')
            self.send_notification(title, content)
        
        # log
        live_room = self.config.get('live_info', 'live_room')
        msg = f'{live_room}\t{previous_signal}\t{live_status}'
        self.logger.debug(msg)


if __name__ == '__main__':
    a = Alert()
    a.controller()

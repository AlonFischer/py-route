#!/usr/bin/env python
# coding=utf-8

from watchdog.observers import Observer
from watchdog.events import *
import time
import os
import shlex
import sys
from pwn import *
import re
import json

CONFIG_FILE = "./config.json"
TASK = "sudo python main.py"
FK_CNC_IP = "3.14.142.149"


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_modified(self, event):
        if event.src_path == CONFIG_FILE:
            print("[+] Updating configs")
            try:
                os.system(TASK)
            except:
                print("error while executing cmd"+ TASK )

class Snort:
    def __init__(self):
        self.client = None
        self.cnc_list = []
        self.start_client()
        self.handle_log()

    def start_client(self):
        # start the client
        args = "snort -A console -i ens33 -u snort -g snort -c /etc/snort/snort.conf"
        args = shlex.split(args)
        self.client = process(args)

    def handle_log(self):
        log = self.client.recv(timeout=0.5)
        if "cnc" in log:
            print log
            log = re.findall(r'^.*cnc.*\{TCP\}\s+(\d+\.\d+\.\d+\.\d+:\d+)\s+->\s+(\d+\.\d+\.\d+\.\d+:\d+)$', log, flags = re.MULTILINE)
            for src, dst in log:
                dst, dport = dst.split(":")
                src, sport = src.split(":")
                if dst not in self.cnc_list:
                    self.add_rule(src, dst)
                    self.cnc_list.append(dst)

    def add_rule(self, host, cnc):
        conf = None
        conn = {"active" : 1,
                "dst" : cnc,
                "proto" : "tcp",
                "target": FK_CNC_IP
                }
        with open(CONFIG_FILE) as json_file:
            conf = json.load(json_file)
            sb = conf['sandbox']
            print host
            if host in sb:
                sb[host]["conn"].append(conn)
        
        with open(CONFIG_FILE, 'w') as outfile:
            json.dump(conf, outfile)

    def __del__(self):
        self.client.kill()


if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler,".",True)
    observer.start()
    snort = Snort()
    try:
        while True:
            time.sleep(2)
            snort.handle_log()

    except KeyboardInterrupt:
        observer.stop()
        observer.join()


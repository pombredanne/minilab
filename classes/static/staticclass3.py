# -*- coding: utf-8 -*-

class Pool():
    conn = None
    
    @staticmethod
    def connection(v):
        Pool.conn = v
"""
計時器模組
用於測量和記錄每一手的耗時
"""

import time


class Timer:
    """計時器"""
    
    def __init__(self):
        """初始化計時器"""
        self.start_time = None
        self.elapsed = 0
    
    def start(self):
        """開始計時"""
        self.start_time = time.time()
    
    def stop(self):
        """停止計時並返回耗時（秒）"""
        if self.start_time is None:
            return 0
        self.elapsed = time.time() - self.start_time
        self.start_time = None
        return self.elapsed
    
    def get_elapsed(self):
        """獲取當前已耗時（秒）"""
        if self.start_time is None:
            return self.elapsed
        return time.time() - self.start_time
    
    def reset(self):
        """重置計時器"""
        self.start_time = None
        self.elapsed = 0

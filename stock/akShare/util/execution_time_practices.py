import time
import datetime
from contextlib import contextmanager
import functools
import logging


# ==================== 方法1: 简单的时间差计算 ====================
def method1_simple_timing():
    """最基础的时间统计方法"""
    start_time = time.time()

    # 模拟一些工作
    time.sleep(2)  # 睡眠2秒

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"方法1 - 简单计时: 程序执行了 {execution_time:.2f} 秒")


# ==================== 方法2: 使用装饰器 ====================
def timing_decorator(func):
    """装饰器方式统计函数执行时间"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行耗时: {end_time - start_time:.4f} 秒")
        return result

    return wrapper


@timing_decorator
def method2_decorated_function():
    """被装饰器包装的函数"""
    time.sleep(1.5)
    return "任务完成"


# ==================== 方法3: 上下文管理器 ====================
@contextmanager
def timer_context(description="代码块"):
    """上下文管理器方式计时"""
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        print(f"{description} 执行时间: {end_time - start_time:.4f} 秒")


def method3_context_manager():
    """使用上下文管理器计时"""
    with timer_context("数据库查询模拟"):
        time.sleep(1)

    with timer_context("数据处理模拟"):
        time.sleep(0.5)


# ==================== 方法4: 使用 datetime 模块 ====================
def method4_datetime_timing():
    """使用 datetime 模块进行更精确的时间统计"""
    start_dt = datetime.datetime.now()

    # 模拟工作
    time.sleep(1.2)

    end_dt = datetime.datetime.now()
    duration = end_dt - start_dt

    print(f"方法4 - datetime计时:")
    print(f"  开始时间: {start_dt}")
    print(f"  结束时间: {end_dt}")
    print(f"  执行时长: {duration}")
    print(f"  总秒数: {duration.total_seconds():.4f} 秒")


# ==================== 方法5: 性能分析工具 ====================
def method5_performance_profiling():
    """使用 cProfile 进行性能分析"""
    import cProfile
    import pstats
    import io

    def sample_function():
        # 模拟复杂计算
        result = 0
        for i in range(1000000):
            result += i ** 2
        return result

    # 创建 profiler
    pr = cProfile.Profile()
    pr.enable()

    # 执行函数
    result = sample_function()

    pr.disable()

    # 输出统计信息
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(10)  # 只显示前10个最耗时的函数

    print("方法5 - 性能分析:")
    print(s.getvalue())


# ==================== 方法6: 日志记录执行时间 ====================
def setup_logger():
    """设置日志记录器"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def method6_logging_timing():
    """结合日志记录执行时间"""
    logger = setup_logger()

    start_time = time.time()
    logger.info("开始执行任务...")

    # 模拟工作
    time.sleep(1.8)

    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"任务完成，执行时间: {execution_time:.2f} 秒")


# ==================== 方法7: 分段计时 ====================
def method7_segment_timing():
    """分段计时，适用于复杂流程"""
    segments = {}

    # 阶段1
    start1 = time.time()
    time.sleep(0.5)
    segments['阶段1'] = time.time() - start1

    # 阶段2
    start2 = time.time()
    time.sleep(0.8)
    segments['阶段2'] = time.time() - start2

    # 阶段3
    start3 = time.time()
    time.sleep(0.3)
    segments['阶段3'] = time.time() - start3

    print("方法7 - 分段计时:")
    total_time = sum(segments.values())
    for segment, duration in segments.items():
        percentage = (duration / total_time) * 100
        print(f"  {segment}: {duration:.3f}秒 ({percentage:.1f}%)")
    print(f"  总计: {total_time:.3f}秒")


# ==================== 最佳实践示例 ====================
class ExecutionTimer:
    """生产环境推荐的计时器类"""

    def __init__(self, name="任务"):
        self.name = name
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.time()
        print(f"[{self.name}] 开始执行...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        execution_time = self.end_time - self.start_time

        if exc_type is None:
            print(f"[{self.name}] 成功完成，耗时: {execution_time:.4f} 秒")
        else:
            print(f"[{self.name}] 执行出错，耗时: {execution_time:.4f} 秒")
            # 重新抛出异常
            return False

    def get_duration(self):
        """获取执行时长"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


def best_practice_example():
    """最佳实践示例"""
    print("\n=== 生产环境最佳实践 ===")

    # 使用上下文管理器
    with ExecutionTimer("数据处理任务") as timer:
        # 模拟复杂业务逻辑
        time.sleep(1)
        # 可以在这里获取中间时长
        mid_time = time.time() - timer.start_time
        print(f"  中途检查: 已执行 {mid_time:.2f} 秒")
        time.sleep(0.5)

    # 获取总执行时间
    total_duration = timer.get_duration()
    print(f"总执行时间: {total_duration:.4f} 秒")


if __name__ == "__main__":
    print("Python 程序执行时间统计方法演示\n")
    print("=" * 50)

    # 执行各种方法
    method1_simple_timing()
    print("-" * 30)

    method2_decorated_function()
    print("-" * 30)

    method3_context_manager()
    print("-" * 30)

    method4_datetime_timing()
    print("-" * 30)

    # method5_performance_profiling()  # 这个会输出很多内容，可选运行
    # print("-" * 30)

    method6_logging_timing()
    print("-" * 30)

    method7_segment_timing()
    print("-" * 30)

    best_practice_example()

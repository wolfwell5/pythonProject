"""
防封策略配置
通过模拟真实浏览器行为来降低被封风险
"""
import random

# ============================================
# 1. User-Agent 池（模拟不同浏览器）
# ============================================
USER_AGENTS = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
    # Edge
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    
    # Firefox
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    
    # Safari
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
]


def get_random_user_agent():
    """随机获取一个 User-Agent"""
    return random.choice(USER_AGENTS)


# ============================================
# 2. 请求头配置
# ============================================
def get_random_headers():
    """生成随机请求头"""
    return {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }


# ============================================
# 3. 时间延迟策略
# ============================================

def short_random_wait():
    """短时间随机等待（1-3 秒）"""
    import time
    wait_time = random.uniform(2, 5)
    time.sleep(wait_time)
    return wait_time


def medium_random_wait():
    """中等时间随机等待（3-8 秒）"""
    import time
    wait_time = random.uniform(4, 10)
    time.sleep(wait_time)
    return wait_time


def long_random_wait():
    """长时间随机等待（10-20 秒）"""
    import time
    wait_time = random.uniform(10, 20)
    time.sleep(wait_time)
    return wait_time


def human_like_wait():
    """模拟人类行为的等待（更自然）"""
    import time
    # 70% 概率等待 2-5 秒，30% 概率等待 8-15 秒
    if random.random() < 0.7:
        wait_time = random.uniform(2, 5)
    else:
        wait_time = random.uniform(8, 15)
    
    time.sleep(wait_time)

    return wait_time


# ============================================
# 4. 批量获取时的智能策略
# ============================================

class AntiBanStrategy:
    """防封策略类"""
    
    def __init__(self):
        self.request_count = 0
        self.last_request_time = None
        self.failed_count = 0
        
    def before_request(self):
        """请求前的准备动作"""
        import time
        
        self.request_count += 1
        
        # 【关键】每 3 次请求后，休息 2-5 分钟（更严格）
        if self.request_count % 3 == 0:
            rest_time = random.uniform(120, 300)
            print(f"🕐 已获取 {self.request_count} 只股票，休息 {rest_time:.0f} 秒...")
            time.sleep(rest_time)
        
        # 如果连续失败 2 次，延长等待时间
        if self.failed_count >= 2:
            wait_time = random.uniform(60, 120)
            print(f"⚠️ 连续失败 {self.failed_count} 次，等待 {wait_time:.0f} 秒...")
            time.sleep(wait_time)
        
        # 人类行为模拟：偶尔快速点击，偶尔慢速点击
        human_like_wait()
    
    def on_success(self):
        """请求成功后的处理"""
        self.failed_count = 0
        print("✅ 获取成功")
    
    def on_failure(self):
        """请求失败后的处理"""
        self.failed_count += 1
        print(f"❌ 获取失败，累计失败 {self.failed_count} 次")
        
        # 失败后立即重置计数器
        if self.failed_count >= 3:
            print("⚠️ 失败次数过多，建议暂停或切换 IP")
    
    def get_stats(self):
        """获取统计信息"""
        return {
            '总请求数': self.request_count,
            '失败次数': self.failed_count,
            '成功率': f"{((self.request_count - self.failed_count) / max(1, self.request_count) * 100):.1f}%"
        }


# ============================================
# 使用示例
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("防封策略演示")
    print("=" * 60)

    # 测试 User-Agent
    print("\n📱 随机 User-Agent:")
    for i in range(3):
        ua = get_random_user_agent()
        print(f"  {i+1}. {ua[:60]}...")

    # 测试等待时间
    print("\n⏳ 测试等待时间:")
    print(f"  短等待：{short_random_wait():.1f}秒")
    print(f"  中等待：{medium_random_wait():.1f}秒")
    print(f"  长等待：{long_random_wait():.1f}秒")
    print(f"  人类行为等待：{human_like_wait():.1f}秒")

    # 测试防封策略
    print("\n🛡️ 防封策略演示:")
    strategy = AntiBanStrategy()

    for i in range(10):
        print(f"\n第 {i+1} 次请求前:")
        strategy.before_request()

        # 模拟成功/失败
        if i != 4 and i != 8:  # 模拟两次失败
            strategy.on_success()
        else:
            strategy.on_failure()

    print("\n📊 最终统计:")
    stats = strategy.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

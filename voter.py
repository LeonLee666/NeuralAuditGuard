import os
import random
import threading
import time
import pymysql
import argparse
import numpy as np
from ratelimiter import RateLimiter

def get_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='123456',
        database='benchbase',
        charset='utf8mb4',
        connect_timeout=5,
        read_timeout=30,
    )

def generate_phone_number():
    """在指定范围内生成随机号码"""
    return random.randint(2010036178, 9899996418)

def query_as_client():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        thread_rate_limiter = RateLimiter(max_calls=rate_limit, period=1)
        
        for _ in range(500000):
            try:
                with thread_rate_limiter:
                    phone_number = generate_phone_number()
                    query = f"SELECT * FROM votes WHERE phone_number = {phone_number};"
                    cursor.execute(query)
                    results = cursor.fetchall()
                    connection.commit()
            except pymysql.MySQLError as err:
                connection.rollback()
                print(f"错误: {err}")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"外部错误: {e}")

def query_as_bot():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        thread_rate_limiter = RateLimiter(max_calls=rate_limit, period=1)
        
        # 从2010036178到9899996418顺序查询
        for phone_number in range(2010036178, 9899996419):
            try:
                with thread_rate_limiter:
                    query = f"SELECT * FROM votes WHERE phone_number = {phone_number};"
                    cursor.execute(query)
                    results = cursor.fetchall()
                    connection.commit()
            except pymysql.MySQLError as err:
                connection.rollback()
                print(f"错误: {err}")
        cursor.close()
        connection.close()
        os._exit(0)
    except Exception as e:
        print(f"外部错误: {e}")
        os._exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='投票查询测试工具')
    parser.add_argument('-c', '--client', 
                       type=int, 
                       default=10,
                       help='普通查询线程数量 (默认: 10)')
    parser.add_argument('-b', '--query_as_bot', 
                       type=int, 
                       default=1,
                       help='爬虫查询线程数量 (默认: 1)')
    parser.add_argument('-r', '--rate_limit',
                       type=int,
                       default=10,
                       help='每秒最大查询次数限制 (默认: 10)')
    
    args = parser.parse_args()
    # 设置全局rate_limit变量
    global rate_limit
    rate_limit = args.rate_limit
    threads = []
    
    # 创建普通查询线程
    for _ in range(args.client):
        thread = threading.Thread(target=query_as_client)
        threads.append(thread)
        thread.start()
    
    # 创建爬虫查询线程
    for _ in range(args.query_as_bot):
        query_as_bot_thread = threading.Thread(target=query_as_bot)
        threads.append(query_as_bot_thread)
        query_as_bot_thread.start()

    # 监控审计日志文件大小
    while True:
        try:
            total_size = 0
            audit_log_dir = '/home/liliang/mysql/data'
            # 遍历目录下所有以 audit_log 开头的文件
            for filename in os.listdir(audit_log_dir):
                if filename.startswith('audit_log'):
                    file_path = os.path.join(audit_log_dir, filename)
                    total_size += os.path.getsize(file_path)
            
            if total_size > 600 * 1024 * 1024:  # 600MB
                print("审计日志文件总大小超过600MB,程序退出")
                os._exit(0)
            time.sleep(1)  # 每秒检查一次
        except FileNotFoundError:
            print("未找到审计日志目录")
            break
        except Exception as e:
            print(f"监控文件大小时发生错误: {e}")
            break

    # 等待所有线程完成
    for thread in threads:
        thread.join()

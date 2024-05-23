from RedisConfig.redis_config import redis_client
import redis

class RedisManager:
    def makeUserActive(self, username):
        try:
            redis_client.sadd('online_user', username)
        except redis.RedisError or Exception as err:
            print(err)
            return None
    
    def makeUserOffline(self, username):
        try:
            redis_client.srem('online_user', username)
        except redis.RedisError or Exception as err:
            print(err)
            return None

    def get_online_users(self):
        try:
            online_users = redis_client.smembers('online_users')
            return online_users
        except redis.RedisError or Exception as err:
            print(f"Redis error: {err}")
            return None
        

    def add_user_connection(self, username, sid):
        try:
            redis_client.hset('user_connections', username, sid)
        except redis.RedisError or Exception as err:
            print(err)

    def remove_user_connections(self, username):
        try:
            redis_client.hdel('user_connections', username)
        except redis.RedisError or Exception as err:
            print(err)

    def get_user_connection(self, username):
        try:
            return redis_client.hget('user_connections', username)
        except Exception or redis.RedisError as err:
            print(err)
            return None

        


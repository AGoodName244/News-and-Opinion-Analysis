import redis

r = redis.Redis(host='localhost', port=6379, db=0)

r.set("test_key", "hello redis")
value = r.get("test_key")

print("Redis returned:", value.decode())

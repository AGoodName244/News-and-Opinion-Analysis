import redis
import json

# r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

QUEUE_NAME = "nlp_task_queue"

def set_task_status(task_id: str, article_id: str, status: str = None, extra: dict = None):
    key = f"task:{task_id}:{article_id}"
    value = {}

    if status is not None:
        value["status"] = status

    if extra:
        for k, v in extra.items():
            if isinstance(v, (dict, list)):
                value[k] = json.dumps(v, ensure_ascii=False)
            else:
                value[k] = str(v)

    if value:
        r.hset(key, mapping=value)
        r.expire(key, 60)

def get_task_status(task_id: str, article_id: str) -> dict:
    key = f"task:{task_id}:{article_id}"
    return r.hgetall(key)

def push_task(task: dict):
    task_json = json.dumps(task, ensure_ascii=False)
    r.lpush(QUEUE_NAME, task_json)

def pop_task_blocking(timeout: int = 5) -> dict | None:
    result = r.brpop(QUEUE_NAME, timeout)
    if result is None:
        return None
    _, task_json = result
    return json.loads(task_json)

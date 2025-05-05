package com.example.nlptaskdispatcher.redis;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

import java.util.Map;

public class RedisClient {

    private static final JedisPool jedisPool = new JedisPool("redis", 6379);

    private static final String NLP_TASK_QUEUE = "nlp_task_queue";

    public static Jedis getResource() {
        return jedisPool.getResource();
    }

    public static void pushTask(String taskJson) {
        try (Jedis jedis = getResource()) {
            jedis.lpush(NLP_TASK_QUEUE, taskJson);
        }
    }

    public static String popTaskBlocking(int timeoutSeconds) {
        try (Jedis jedis = getResource()) {
            var result = jedis.brpop(timeoutSeconds, NLP_TASK_QUEUE);
            if (result != null && result.size() > 1) {
                return result.get(1);
            } else {
                return null;
            }
        }
    }

    public static void setTaskOverallStatus(String taskId, String status) {
        try (Jedis jedis = jedisPool.getResource()) {
            jedis.setex("task: " + taskId, 3600, status);
        }
    }

    public static String getTaskOverallStatus(String taskId) {
        try (Jedis jedis = jedisPool.getResource()) {
            return jedis.get("task: " + taskId);
        }
    }

    public static void setTaskStatus(String taskId, String articleId, Map<String, String> fields, int expireSeconds) {
        String key = String.format("task:%s:%s", taskId, articleId);
        try (Jedis jedis = getResource()) {
            jedis.hset(key, fields);
            jedis.expire(key, expireSeconds);
        }
    }

    public static Map<String, String> getTaskStatus(String taskId, String articleId) {
        String key = String.format("task:%s:%s", taskId, articleId);
        try (Jedis jedis = getResource()) {
            return jedis.hgetAll(key);
        }
    }

    public static void deleteTaskStatus(String taskId, String articleId) {
        String key = String.format("task:%s:%s", taskId, articleId);
        try (Jedis jedis = getResource()) {
            jedis.del(key);
        }
    }
}

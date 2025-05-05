package com.example.nlptaskdispatcher.service;

import com.example.nlptaskdispatcher.model.TaskResult;
import com.example.nlptaskdispatcher.repository.TaskResultProjection;
import com.example.nlptaskdispatcher.repository.TaskResultRepository;
import com.example.nlptaskdispatcher.redis.RedisClient;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.*;

import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Service
public class TaskService {

    @Autowired
    private TaskResultRepository taskResultRepository;

    private final ExecutorService executorService = Executors.newFixedThreadPool(5);

    private final RestTemplate restTemplate = new RestTemplate();

    private static final String CRAWLER_API_URL = "http://python-crawler:8002/api/crawl_and_analyze";
    private static final String NLP_API_URL = "http://python-nlp:8001/enqueue";

    private final ObjectMapper objectMapper = new ObjectMapper(); // 处理 JSON

    public String submitTask(String keyword, String depth) {
        String taskId = UUID.randomUUID().toString();
//        new Thread(() -> missionDispatch(taskId, keyword, depth)).start();
        executorService.submit(() -> missionDispatch(taskId, keyword, depth));
        return taskId;
    }

    private void missionDispatch(String taskId, String keyword, String depth) {
        try {
            Map<String, Object> payload = Map.of(
                    "task_id", taskId,
                    "keyword", keyword,
                    "source_name", "google_news",
                    "source_url", "https://news.google.com",
                    "depth", depth
            );
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> request = new HttpEntity<>(payload, headers);
            ResponseEntity<Map> response = restTemplate.postForEntity(CRAWLER_API_URL, request, Map.class);

            List<Map<String, Object>> articles = (List<Map<String, Object>>) response.getBody().get("articles");

            if (articles == null || articles.isEmpty()) {
                System.err.println("[Async Task] No articles fetched for keyword: " + keyword);
                throw new RuntimeException("No articles fetched for keyword: " + keyword);
            }

            List<Map<String, Object>> nlpTasks = new ArrayList<>();
            for (Map<String, Object> article : articles) {
                String articleId = UUID.randomUUID().toString();
                String title = (String) article.get("title");
                String text = (String) article.get("text");
                String url = (String) article.get("url");

                Map<String, Object> nlpTask = Map.of(
                        "task_id", taskId,
                        "article_id", articleId,
                        "text", (title != null ? title : "") + " " + (text != null ? text : ""),
                        "url", (url != null ? url : ""),
                        "title", (title != null ? title : "")
                );
                nlpTasks.add(nlpTask);
                RedisClient.pushTask(serializeToJson(nlpTask));
            }
            monitorAndSave(taskId, nlpTasks);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    private void monitorAndSave(String taskId, List<Map<String, Object>> nlpTasks) {
        try {
            System.out.println("[Monitor] Start monitoring task " + taskId);
//            System.out.println("[Monitor] articles: " + articles);

            Map<String, Map<String, Object>> articleInfoMap = new HashMap<>();
            for (Map<String, Object> article : nlpTasks) {
                String articleId = (String) article.get("article_id");
                articleInfoMap.put(articleId, article);
            }

            Set<String> pendingArticles = new HashSet<>(articleInfoMap.keySet());
            RedisClient.setTaskOverallStatus(taskId, "processing");
            int maxRetries = 30; // 最多等 30 次（约 60秒）
            while (maxRetries-- > 0) {
                System.out.println("[Monitor] Max retries left: " + maxRetries);
                Iterator<String> iter = pendingArticles.iterator();
                while (iter.hasNext()) {
                    String articleId = iter.next();
                    Map<String, String> status = RedisClient.getTaskStatus(taskId, articleId);

                    if (status != null && "done".equals(status.get("status"))) {
                        Map<String, Object> articleInfo = articleInfoMap.get(articleId);
                        saveOneResult(taskId, articleId, status, articleInfo);
                        iter.remove();
                    } else if (status != null && "error".equals(status.get("status"))) {
                        System.out.println("[Monitor] Task failed for article " + articleId);
                        iter.remove();
                    }
                }

                if (pendingArticles.isEmpty()) {
                    System.out.println("[Monitor] All articles processed for task " + taskId);
                    break;
                }

                TimeUnit.SECONDS.sleep(2);
            }

            if (!pendingArticles.isEmpty()) {
                System.out.println("[Monitor] Timeout waiting for some articles: " + pendingArticles);
            }
            RedisClient.setTaskOverallStatus(taskId, "done");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void saveOneResult(String taskId, String articleId, Map<String, String> statusInfo, Map<String, Object> articleInfo) {
//        System.out.println("[Monitor] Saving task result for article " + articleId + ": " + statusInfo.keySet() + ": " + articleInfo.keySet());
        TaskResult result = new TaskResult();
        String createTime = new Date().toString();
        System.out.println("taskId: " + taskId + " articleId: " + articleId +
                " content: " + (String)articleInfo.get("text") + " summary: " + statusInfo.get("summary") +
                " sentiment: " + statusInfo.get("sentiment") +
                " keyword: " + (String)articleInfo.get("keyword") +
                " url: " + (String)articleInfo.get("url") +
                " title: " + (String)articleInfo.get("title") +
                " createAt: " + createTime);
        result.setTaskId(taskId);
        result.setArticleId(articleId);
        result.setContent((String)articleInfo.get("text"));
        result.setSummary(statusInfo.get("summary"));
        result.setSentiment(statusInfo.get("sentiment"));
        result.setStatus("done");
        result.setCreatedAt(createTime);

//        result.setKeyword((String)articleInfo.get("keyword"));
        String keywordsJson = statusInfo.get("keywords");
        result.setKeyword(keywordsJson);
        result.setTitle((String)articleInfo.get("title"));
        result.setUrl((String)articleInfo.get("url"));
        result.setSource("google_news");

        taskResultRepository.save(result);
    }

    public List<TaskResultProjection> getResultsByTaskId(String taskId) {
        return taskResultRepository.findByTaskId(taskId);
    }

    private String serializeToJson(Object obj) {
        try {
            return objectMapper.writeValueAsString(obj);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
    public Map<String, String> getCurrentStatuses(String taskId, List<String> articleIds) {
        Map<String, String> statuses = new HashMap<>();
        for (String articleId : articleIds) {
            Map<String, String> info = RedisClient.getTaskStatus(taskId, articleId);
            if (info != null && info.containsKey("status")) {
                statuses.put(articleId, info.get("status"));
            } else {
                statuses.put(articleId, "unknown");
            }
        }
        return statuses;
    }

}

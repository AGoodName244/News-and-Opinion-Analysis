package com.example.nlptaskdispatcher.repository;

public interface TaskResultProjection {
    String getTaskId();
    String getArticleId();
    String getTitle();
    String getSummary();
    String getSentiment();
    String getCreatedAt();
    String getUrl();
}

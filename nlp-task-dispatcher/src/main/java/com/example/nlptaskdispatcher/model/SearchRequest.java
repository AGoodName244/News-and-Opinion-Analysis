package com.example.nlptaskdispatcher.model;

public class SearchRequest {
    private String keyword;
    private String depth;


    public SearchRequest() {}

    public SearchRequest(String keyword, String depth) {
        this.keyword = keyword;
        this.depth = depth;
    }

    public String getKeyword() {
        return keyword;
    }

    public void setKeyword(String keyword) {
        this.keyword = keyword;
    }

    public String getDepth() {
        return depth;
    }

    public void setDepth(String depth) {
        this.depth = depth;
    }
}

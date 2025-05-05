package com.example.nlptaskdispatcher.controller;

import com.example.nlptaskdispatcher.model.TaskResult;
import com.example.nlptaskdispatcher.model.SearchRequest;
import com.example.nlptaskdispatcher.redis.RedisClient;
import com.example.nlptaskdispatcher.repository.TaskResultProjection;
import com.example.nlptaskdispatcher.service.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class TaskController {

    @Autowired
    private TaskService taskService;

    @PostMapping("/search")
    public TaskResponse handleSearch(@RequestBody SearchRequest request) {
        String taskId = taskService.submitTask(request.getKeyword(), request.getDepth());
        return new TaskResponse(taskId, request.getKeyword(), request.getDepth(), "processing", Instant.now().toString());
    }

    @GetMapping("/result/{taskId}")
    public ResponseEntity<?> getResults(@PathVariable String taskId) {
        String status = RedisClient.getTaskOverallStatus(taskId);
//        if (status == null || "processing".equals(status)) {
//            return ResponseEntity.status(HttpStatus.ACCEPTED)
//                    .body("Task is still processing or does not exist");
//        }
        if (status == null) {
            return ResponseEntity.status(HttpStatus.NO_CONTENT)
                    .body("Task is on the way or timeout");
        }
        else if (status.equals("processing")) {
            return ResponseEntity.status(HttpStatus.ACCEPTED)
                    .body("Task is still processing");
        }
        List<TaskResultProjection> results = taskService.getResultsByTaskId(taskId);
        return ResponseEntity.ok(results);
    }

    @GetMapping("/status/{taskId}")
    public Map<String, String> checkStatus(
            @PathVariable String taskId,
            @RequestParam List<String> articleIds
    ) {
        return taskService.getCurrentStatuses(taskId, articleIds);
    }

    static class TaskResponse {
        public String task_id;
        public String keyword;
        public String depth;
        public String status;
        public String created_at;

        public TaskResponse(String task_id, String keyword, String depth, String status, String created_at) {
            this.task_id = task_id;
            this.keyword = keyword;
            this.depth = depth;
            this.status = status;
            this.created_at = created_at;
        }
    }

    static class TaskStatus {
        public String task_id;
        public String status;

        public TaskStatus(String task_id, String status) {
            this.task_id = task_id;
            this.status = status;
        }
    }

}

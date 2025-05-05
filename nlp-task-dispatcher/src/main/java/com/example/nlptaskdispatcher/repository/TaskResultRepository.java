package com.example.nlptaskdispatcher.repository;

import com.example.nlptaskdispatcher.model.TaskResult;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface TaskResultRepository extends JpaRepository<TaskResult, Long> {

//    List<TaskResult> findByTaskId(String taskId);
    List<TaskResultProjection> findByTaskId(String taskId);
}

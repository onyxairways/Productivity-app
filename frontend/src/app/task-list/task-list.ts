import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { TaskService, Task } from '../task.service';

@Component({
  selector: 'app-task-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './task-list.html',
  styleUrl: './task-list.css'
})
export class TaskListComponent implements OnInit {
  tasks = signal<Task[]>([]);

  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
    this.taskService.getTasks().subscribe(tasks => {
      this.tasks.set(tasks);
    });
  }

  addTask(title: string): void {
    if (!title.trim()) return;
    this.taskService.createTask(title).subscribe(task => {
      this.tasks.update(current => [...current, task]);
    });
  }

  toggleComplete(task: Task): void {
    this.taskService.updateTask(task.id, !task.completed).subscribe(updated => {
      this.tasks.update(current =>
        current.map(t => t.id === updated.id ? updated : t)
      );
    });
  }

  deleteTask(id: number): void {
    this.taskService.deleteTask(id).subscribe(() => {
      this.tasks.update(current => current.filter(t => t.id !== id));
    });
  }
}

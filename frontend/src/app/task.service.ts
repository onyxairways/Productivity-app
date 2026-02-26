import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getTasks(): Observable<Task[]> {
    return this.http.get<Task[]>(`${this.apiUrl}/tasks`);
  }

  getTask(id: number): Observable<Task> {
    return this.http.get<Task>(`${this.apiUrl}/tasks/${id}`);
  }

  createTask(title: string, description?: string): Observable<Task> {
    return this.http.post<Task>(`${this.apiUrl}/tasks`, { title, description });
  }

  updateTask(id: number, completed: boolean): Observable<Task> {
    return this.http.put<Task>(`${this.apiUrl}/tasks/${id}?completed=${completed}`, {});
  }

  updateDescription(id: number, description: string): Observable<Task> {
    return this.http.patch<Task>(`${this.apiUrl}/tasks/${id}`, { description });
  }


  deleteTask(id: number): Observable<Task> {
    return this.http.delete<Task>(`${this.apiUrl}/tasks/${id}`);
  }
}

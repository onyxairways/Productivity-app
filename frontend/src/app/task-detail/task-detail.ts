import { Component, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TaskService, Task } from '../task.service';

@Component({
    selector: 'app-task-detail',
    standalone: true,
    imports: [CommonModule, RouterLink, FormsModule],
    templateUrl: './task-detail.html',
    styleUrl: './task-detail.css'
})
export class TaskDetailComponent implements OnInit {
    task = signal<Task | null>(null);
    description = signal('');
    questions = signal<string[]>([]);
    answers = signal<string[]>([]);


    constructor(
        private route: ActivatedRoute,
        private taskService: TaskService
    ) { }

    ngOnInit(): void {
        const id = Number(this.route.snapshot.paramMap.get('id'));
        this.taskService.getTask(id).subscribe(task => {
            this.task.set(task);
            this.description.set(task.description ?? '');
        });
    }

    saveDescription(): void {
        const task = this.task();
        if (!task) return;
        this.taskService.updateDescription(task.id, this.description()).subscribe(updated => {
            this.task.set(updated);
        });
    }

    fetchQuestions(): void {
        const task = this.task();
        if (!task) return;
        this.taskService.getQuestions(task.id).subscribe(result => {
            this.questions.set(result.questions);
            this.answers.set(result.questions.map(() => ''));
        });
    }

    updateAnswer(index: number, value: string): void {
        const updated = [...this.answers()];
        updated[index] = value;
        this.answers.set(updated);
    }

    generateDescription(): void {
        const task = this.task();
        if (!task) return;
        this.taskService.suggestDescription(task.id, this.answers()).subscribe(result => {
            this.description.set(result.suggestion);
            this.questions.set([]);
            this.answers.set([]);
        });
    }


}

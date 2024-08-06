import type { TaskInterface } from "./tasks.interface";

export class Task implements TaskInterface{
    id: string;
    title: string;
    description: string;
    startTime: Date;
    endTime: Date;
    date: Date;
    timeString: string;
    completed: boolean;
    constructor(properties: Partial<TaskInterface>) {
        this.id = properties.id || "";
        this.title = properties.title || "";
        this.description = properties.description || "";
        this.startTime = properties.startTime || new Date();
        this.endTime = properties.endTime || new Date();
        this.date = properties.date || new Date();
        this.timeString = properties.timeString || "";
        this.completed = properties.completed || false;
    }
}

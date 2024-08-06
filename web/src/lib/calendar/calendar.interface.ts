import type { Task } from "$lib/tasks/task.model";
import type { Moment } from "moment";
export interface Day {
    id: string;
    date: Date;
    momentDate?: Moment;
    dayOfWeek: string; // Mon, Tue, Wed, Thu, Fri, Sat, Sun
    dayOfMonth: string; // 9
    month: string; // Jun
    year: string; // 2024
    tasks: Task[];
}

export interface Week {
    label: string; // Jun 9 - 15
    mappedDays: Record<string, Day>;
}


export interface CalendarInterface
{
    days: Day[];
    weeks: Week[];
    mappedDays: Record<string, Day>;
}
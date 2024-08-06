export interface TaskInterface {
    id: string;
    title: string;
    description: string;
    date: Date;
    startTime: Date;
    endTime: Date;
    timeString: string; // 12:00 -- 1:00 PM
    completed: boolean;
}
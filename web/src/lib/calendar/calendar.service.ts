import type {  Day } from "./calendar.interface";
import moment from "moment";
import { Calendar } from "./calendar.model";
export class CalendarService {
    private readonly calendar: Calendar;

    constructor() {
        this.calendar = new Calendar();
    }

    getCalendar() {
        return this.calendar;
    }

    generateAroundDate(date: Date, offsetPrevious: number = 1, offsetNext: number = 1) {
        return this.generateRange(date, offsetPrevious, offsetNext);
    }

    generateBefore(date: Date, offset: number = 2) {
        return this.generateRange(date, offset, 0);
    }

    generateAfter(date: Date, offset: number = 2) {
        return this.generateRange(date, 0, offset);
    }

    private generateRange(date: Date, previousOffset: number, nextOffset: number) {
        const start = new Date(date.getFullYear(), date.getMonth() - previousOffset, 1);
        const end = new Date(date.getFullYear(), date.getMonth() + nextOffset, 0);
        const days = this.generateDays(start, end);
        return this.calendar.addDays(days);
    }

    generateDays(start: Date, end: Date): Day[] {
        const days: Day[] = [];
        while (start <= end) {
            const momentDate = moment(start);
            days.push({
                id: momentDate.format("YYYYMMDD"),
                date: momentDate.toDate(),
                momentDate: momentDate,
                dayOfWeek: momentDate.format("ddd"),
                dayOfMonth: momentDate.format("D"),
                month: momentDate.format("MMM"),
                year: momentDate.format("YYYY"),
                tasks: [],
            });
            start.setDate(start.getDate() + 1);
        }
        return days;
    }

    

    
}

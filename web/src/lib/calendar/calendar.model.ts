import type { CalendarInterface, Day, Week } from "./calendar.interface";

export class Calendar implements CalendarInterface {
    days: Day[] = [];
    mappedDays: Record<string, Day> = {};
    weeks: Week[] = [];

    toObject() {
        this.days.forEach((day) => {
            delete day.momentDate
        });
        return {
            days: this.days,
            mappedDays: this.mappedDays,
            weeks: this.weeks
        }
    }
    
    addDays(days: Day[]) {
        days.forEach((day) => {
            if(!this.mappedDays[day.id]) {
                this.mappedDays[day.id] = day;
                this.days.push(day);
            }
        });
        this.sortDays();
        this.weeks = this.generateWeeks(this.days);
    }

    sortDays() {
        this.days.sort((a, b) => a.momentDate?.diff(b.momentDate) || 0);
    }

    generateWeeks(days: Day[]): Week[] {
        const weeks: Record<string, Week> = {};
        for (let i = 0; i < days.length; i += 1) {
            const weekLabel = days[i].momentDate?.format("W YYYY") || "";
            if (!weeks[weekLabel]) {
                weeks[weekLabel] = this.createWeekFromDay(days[i]);
            }
            weeks[weekLabel].mappedDays[days[i].id] = days[i];
        }
        return Object.values(weeks);
    }

    createWeekFromDay(day: Day): Week {
        const monday = day.momentDate?.clone().weekday(1);
        const sunday = day.momentDate?.clone().weekday(7);
        const initialMonth = monday?.format("MMM") || "";
        const initialDay = monday?.format("D") || "";
        const finalMonth = sunday?.format("MMM") || "";
        const finalDay = sunday?.format("D") || "";
        return {
            label: `${initialMonth} ${initialDay} - ${finalMonth === initialMonth ? finalDay : `${finalMonth} ${finalDay}`}`,
            mappedDays: {},
        };
    }

}
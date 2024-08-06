import { it, describe, expect } from "vitest";
import { CalendarService } from "./calendar.service";
import type { Day } from "./calendar.interface";
import moment from "moment";
import { Task } from "$lib/tasks/task.model";
describe("CalendarService", () => {
  it("should generate weeks", () => {
    const calendarService = new CalendarService();
    const date = new Date(2024, 4, 1)
    const momentDate = moment(date)
    const day: Day = {
        id: "20240501",
        date,
        momentDate,
        dayOfWeek: "Monday",
        dayOfMonth: "1",
        month: "May",
        year: "2024",
        tasks: [],
    }
    const weeks = calendarService.getCalendar().generateWeeks([day]);
    expect(weeks[0].label).toBe("Apr 29 - May 5");
    expect(weeks[0].mappedDays["20240501"].id).toBe("20240501");
  });

  it("should generate days for a given range", () => {
    const calendarService = new CalendarService();
    const start = new Date(2024, 4, 1)
    const end = new Date(2024, 4, 10)
    const days = calendarService.generateDays(start, end);
    expect(days).toHaveLength(10);
    expect(days[0].id).toBe("20240501");
  });

  it("should create a calendar around a date", () => {
    const calendarService = new CalendarService();
    const date = new Date(2024, 4, 1)
    calendarService.generateAroundDate(date);
    const calendar = calendarService.getCalendar();
    expect(calendar.weeks[0].label).toBe("Apr 1 - 7");
    expect(calendar.weeks[calendar.weeks.length - 1].label).toBe("May 27 - Jun 2");
    expect(calendar.mappedDays["20240501"].id).toBe("20240501");
  });

  it("should append days to an existing calendar", () => {
    const calendarService = new CalendarService();
    const date = new Date(2024, 4, 1)
    calendarService.generateAroundDate(date);
    const calendar = calendarService.getCalendar();
    calendar.mappedDays["20240531"].tasks.push(new Task({
        id: "1",
    }))
    const newDate = new Date(2024,  5, 10)
    calendarService.generateAroundDate(newDate);
    expect(calendar.weeks[0].label).toBe("Apr 1 - 7");
    expect(calendar.weeks[calendar.weeks.length - 1].label).toBe("Jun 24 - 30");
    expect(calendar.mappedDays["20240531"].tasks).toHaveLength(1);
    expect(calendar.mappedDays["20240531"].tasks[0].id).toBe("1");
  });

  it("should sort days by date", () => {
    const calendarService = new CalendarService()
    const calendar = calendarService.getCalendar();
    calendar.addDays(calendarService.generateDays( new Date(2024, 4, 1), new Date(2024, 4, 10)));  
    calendar.addDays(calendarService.generateDays( new Date(2024, 3, 11), new Date(2024, 3, 20)));  
    expect(calendar.days[0].id).toBe("20240411");
    expect(calendar.days[calendar.days.length - 1].id).toBe("20240510");
  });
});
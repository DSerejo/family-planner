import { CalendarService } from "$lib/calendar/calendar.service"

export const load = async () => {
    const calendarService = new CalendarService();
    calendarService.generateAroundDate(new Date(), 3);
    return {
        calendar: calendarService.getCalendar().toObject()
    }
}
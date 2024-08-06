<script lang="ts">
    import type { PageData } from './$types';

    export let data: PageData;
    console.log(data.calendar);
</script>

<div>
    {#each data.calendar.weeks as week}
        <div>{week.label}</div>
        {#each Object.values(week.mappedDays) as day}
            <div>{day.dayOfWeek} {day.dayOfMonth}</div>
        {/each}
    {/each}
</div>
<script lang="ts">
	import TextField from '@smui/textfield';
    import Button from '@smui/button';
	import { enhance } from '$app/forms';
    import { goto } from '$app/navigation';
    export let disabled = false;
    let formElement: HTMLFormElement;
    export let slug: string;

    function onSubmit() {
        disabled = true;
        formElement.submit();
    }
    function onCancel() {
        goto('/family/' + slug);
    }
</script>

<form method="post" aria-label="form" bind:this={formElement}>
    <TextField value='' input$name="name" label="Name" placeholder="Name" required />
    <TextField value='' input$name="email" label="Email" placeholder="Email" />
    <Button type="submit" on:click={onSubmit} disabled={disabled}>Add Member</Button>
    <Button on:click={onCancel}>Cancel</Button>
</form>
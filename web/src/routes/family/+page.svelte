<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import type { PageData, ActionData } from './$types';
	import CreateFamilyForm from '$lib/family/create-family-form.svelte';

	export let data: PageData;
	// export let form: ActionData;
	onMount(() => {
		if (!data.googleSession) {
			goto('/');
		}

		// if (form?.success) {
		// 	goto('/test');
		// }
	});
</script>

{#if data?.googleSession}
	<div>Family</div>
	{#if data?.family?.length}
		<div>
			{#each data.family as family}
				<div>{family.name}</div>
			{/each}
		</div>
	{:else}
		<CreateFamilyForm />
	{/if}
{/if}

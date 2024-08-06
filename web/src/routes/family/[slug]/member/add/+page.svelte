<script lang="ts">
	import AddMemberForm from '$lib/family/add-member-form.svelte';
	import Snackbar, { Label, Actions } from '@smui/snackbar';
	import IconButton from '@smui/icon-button';
	import Button from '@smui/button';
	import type { PageData } from './$types';
	import { onMount } from 'svelte';
	export let data: PageData;
	let disabled = false;
	let snackbar: Snackbar;

	onMount(() => {
		if (data.error) {
			disabled = false;
			snackbar.label = data.error
			snackbar.open()
		}
	})
	
</script>

<Snackbar bind:this={snackbar} leading={true} labelText={data.error}>
	<Label/>
	<Actions>
		<IconButton class="material-symbols-outlined" title="Dismiss">close</IconButton>
	</Actions>
</Snackbar>

<AddMemberForm disabled={disabled} slug={data.familyId} />

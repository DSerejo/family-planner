<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import type { PageData, ActionData } from './$types';
	import CreateFamilyForm from '$lib/family/create-family-form.svelte';
	import Button from '@smui/button';
	import { invalidateAll } from '$app/navigation';
    import ConfirmationDialog from '$lib/common/confirmation-dialog.svelte';
	import { createConfirmationDialogComponent } from '$lib/common/confirmation-dialog.service';
import Snackbar, {Label} from '@smui/snackbar';

	export let data: PageData;
	let confirmationDialog: {component: typeof ConfirmationDialog, props: any} | undefined;
    let snackbar: Snackbar;
	onMount(() => {
		if (!data.googleSession) {
			goto('/');
		}
	});
	async function onDeleteClick(familyId: string) {
        confirmationDialog = createConfirmationDialogComponent({
            title: 'Delete family',
            content: 'Are you sure you want to delete this family?',
            confirmText: 'Delete',
            cancelText: 'Cancel',
            open: true,
            onConfirm: () => deleteFamily(familyId),
            onCancel: () => {
                confirmationDialog = undefined;
            }
        });
    }
	let deleteFamily = async (familyId: string) => {
		const formData = new FormData();
		formData.set('familyId', familyId);
		await fetch('/family?/delete', {
			method: 'POST',
			body: formData
		});
		
		snackbar.close();
		snackbar.getLabelElement().innerHTML = 'Family deleted';
		snackbar.open();
		await invalidateAll();
	};

	let setDefaultFamily = async (familyId: string) => {
		snackbar.close();
		window.localStorage.setItem('defaultFamilyId', familyId);
		snackbar.getLabelElement().innerHTML = 'Default family set';
		snackbar.open();
	};

</script>

{#if data?.googleSession}
	<div class="flex flex-col gap-4 w-100">
		<div class="text-2xl font-bold">My Families</div>
		{#if data?.families?.length}
			<div class="flex flex-col gap-2">
				{#each data.families as family}
					<div class="flex justify-between items-center">
						<a href={`/family/${family.id}`}>{family.name}</a>
						<div class="flex gap-2">
							<Button on:click={() => setDefaultFamily(family.id)}>Use</Button>
							<Button on:click={() => onDeleteClick(family.id)}>Delete</Button>
						</div>
					</div>
				{/each}
			</div>
			<Button href="/family/create">Create Family</Button>
		{:else}
			<CreateFamilyForm />
		{/if}
	</div>
{/if}
<svelte:component this={confirmationDialog?.component} {...confirmationDialog?.props} />
<Snackbar bind:this={snackbar}>
    <Label/>
</Snackbar>
<style lang="scss">
</style>
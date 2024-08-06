<script lang="ts">
	import type { FamilyMember } from '$lib/family/family.interface';
    import type { PageData } from './$types';
    import { goto, invalidateAll } from '$app/navigation';
    import ConfirmationDialog from '$lib/common/confirmation-dialog.svelte';
    import Button, { Label as ButtonLabel } from '@smui/button';
    import { createConfirmationDialogComponent } from '$lib/common/confirmation-dialog.service';
    import Snackbar, {Label} from '@smui/snackbar';
	export let data: PageData;
    let members: FamilyMember[] = [];
    let snackbar: Snackbar;
    let confirmationDialog: {component: typeof ConfirmationDialog, props: any} | undefined;
    $: members = data.family?.members || []

    async function onDeleteClick(memberId: string) {
        memberId = memberId;
        confirmationDialog = createConfirmationDialogComponent({
            title: 'Delete member',
            content: 'Are you sure you want to delete this member?',
            confirmText: 'Delete',
            cancelText: 'Cancel',
            open: true,
            onConfirm: () => deleteFamilyMember(memberId),
            onCancel: () => {
                confirmationDialog = undefined;
            }
        });
    }
    async function deleteFamilyMember(memberId: string) {
        const formData = new FormData();
        formData.append('memberId', memberId);
        await fetch('/family/' + data.family?.id + '?/deleteFamilyMember', {
            method: 'POST',
            body: formData
        });
        invalidateAll();
        snackbar.open();
    }

</script>

<div class="family-members">
    <div class="family-members-title">Family members</div>
    {#each members as member}
        <div class="family-member">
            <div>{member.name}</div>
            <Button on:click={() => onDeleteClick(member.id)}>Delete</Button>
        </div>
    {/each}
    <Button on:click={() => {
        goto('/family/' + data.family?.id + '/member/add')
    }}>Add member</Button>
</div>
<svelte:component this={confirmationDialog?.component} {...confirmationDialog?.props} />
<Snackbar bind:this={snackbar}>
    <Label>Member deleted</Label>
</Snackbar>

<style>
    .family-members {
        display: flex;
        flex-direction: column;
        gap: 10px;
        width: 100%;
    }
    .family-members-title {
        font-size: 24px;
        font-weight: 500;
        text-align: center;
        margin-bottom: 10px;
    }
    .family-member {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
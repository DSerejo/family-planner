<script lang="ts">
    import Dialog, { Title, Content, Actions } from '@smui/dialog';
    import Button, { Label as ButtonLabel } from '@smui/button';

    export let open = false;
    export let title = 'Confirmation';
    export let content = 'Are you sure?';
    export let confirmText = 'Confirm';
    export let cancelText = 'Cancel';

    export let onConfirm = () => {};
    export let onCancel = () => {};
    
    let onCancelClick = () => {
        onCancel();
        open = false;
    }
    let onConfirmClick = () => {
        onConfirm();
        open = false;
    }
</script>

<Dialog
  bind:open={open}
  aria-labelledby="simple-title"
  aria-describedby="simple-content"
>
  <!-- Title cannot contain leading whitespace due to mdc-typography-baseline-top() -->
  <Title id="simple-title">{title}</Title>
  <Content id="simple-content">{content}</Content>
  <Actions>
    <Button on:click={onCancelClick}>
      <ButtonLabel>{cancelText}</ButtonLabel>
    </Button>
    <Button on:click={onConfirmClick}>
      <ButtonLabel>{confirmText}</ButtonLabel>
    </Button>
  </Actions>
</Dialog>
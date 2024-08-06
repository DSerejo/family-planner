import ConfirmationDialog from './confirmation-dialog.svelte';

export interface ConfirmationDialogOptions {
    title?: string;
    content?: string;
    confirmText?: string;
    cancelText?: string;
    onConfirm?: () => void;
    onCancel?: () => void;
    open?: boolean;
}

export function createConfirmationDialogComponent(options: ConfirmationDialogOptions) {
    return {
        component: ConfirmationDialog,
        props: {
            title: options.title,
            content: options.content,
            confirmText: options.confirmText,
            cancelText: options.cancelText,
            onConfirm: options.onConfirm,
            onCancel: options.onCancel,
            open: options.open
        }
    }
}
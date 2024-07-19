import { signOut as authSignOut } from '@auth/sveltekit/client';

export const signOut = async () => {
    await fetch('/api/session/signout');
    await authSignOut();
};
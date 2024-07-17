
import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/svelte';
import Page from './+page.svelte';
import * as authClient from '@auth/sveltekit/client';

vi.mock('@auth/sveltekit/client', () => ({
	signIn: vi.fn(),
	signOut: vi.fn()
}));

describe('Page', () => {
	it('should render the welcome message', () => {
		const { getByText } = render(Page, { data: { googleSession: null } });

		expect(getByText('Welcome to SvelteKit')).toBeDefined();
		expect(getByText('You are not signed in')).toBeDefined();
	});

	it('should call signIn on button click when not signed in', async () => {
		const { getByText } = render(Page, { data: { googleSession: null } });

		const signInButton = getByText('Sign In with Google');
		await fireEvent.click(signInButton);

		expect(authClient.signIn).toHaveBeenCalledWith('google');
	});

	it('should render user info when signed in', () => {
		const user = { name: 'John Doe' };
		const { getByText } = render(Page, { data: { googleSession: { user } } });

		expect(getByText('Signed in as')).toBeDefined();
		expect(getByText('John Doe')).toBeDefined();
	});

	it('should call signOut on button click when signed in', async () => {
		const user = { name: 'John Doe' };
		const { getByText } = render(Page, { data: { googleSession: { user } } });

		const signOutButton = getByText('Sign out');
		await fireEvent.click(signOutButton);

		expect(authClient.signOut).toHaveBeenCalled();
	});
});

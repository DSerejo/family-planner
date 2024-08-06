import { render, fireEvent } from '@testing-library/svelte';
import MemberAddPage from './+page.svelte';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { goto } from '$app/navigation';

vi.mock('$app/navigation', () => ({
  goto: vi.fn()
}));

describe('MemberAddPage', () => {
  it('should display error message in snackbar when data.error is present', async () => {
    const { getByText, component } = render(MemberAddPage, {
      props: {
        data: { error: 'Test error message', googleSession: null, session: null, familyId: '1' }
      }
    });

    // Check if the snackbar is displayed with the error message
    expect(getByText('Test error message')).toBeTruthy();
  });

  it('should not display error message in snackbar when there is no error', async () => {
    const { queryByText } = render(MemberAddPage, {
      props: {
        data: { error: null, googleSession: null, session: null, familyId: '1' }
      }
    });

    // Check if the snackbar is not displayed
    expect(queryByText('Test error message')).toBeNull();
  });

  it('should submit form when button is clicked', async () => {
    const { getByText, getByRole } = render(MemberAddPage, {
      props: {
        data: { error: null, googleSession: null, session: null, familyId: '1' }
      }
    });
    const formElement = getByRole('form') as HTMLFormElement;
    const submitSpy = vi.spyOn(formElement, 'submit');

    const button = getByText('Add Member');
    await fireEvent.click(button);
    expect(submitSpy).toHaveBeenCalled();
    expect(button.hasAttribute('disabled')).toBeTruthy();

  });

  it('should redirect to family page when cancel button is clicked', async () => {
    const { getByText } = render(MemberAddPage, {
      props: {
        data: { error: null, googleSession: null, session: null, familyId: '1' }
      }
    });
    const button = getByText('Cancel');
    await fireEvent.click(button);
    expect(goto).toHaveBeenCalledWith('/family/1');
  });
});

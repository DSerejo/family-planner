import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, fireEvent, waitFor } from '@testing-library/svelte';
import FamilyDetailsPage from './+page.svelte';
import type { PageData } from './$types';
import { goto } from '$app/navigation';

global.fetch = vi.fn() as unknown as typeof fetch;
vi.mock('$app/navigation', () => ({
    goto: vi.fn(),
    invalidateAll: vi.fn()
}));
describe('FamilyDetailsPage', () => {
    let props: {data: PageData};
    beforeEach(() => {
        
        props = {
            data: { googleSession: null, session: null, family: { id: '1', name: 'Test Family', members: [
                { id: '1', name: 'Test Member', email: 'test@test.com' }
              ] } }
        };
    });
    it('should render', () => {
        const { getByText } = render(FamilyDetailsPage, {
            props: props
        });
        expect(getByText('Family members')).toBeDefined();
    });

    it('should list family members', () => {
        const { getByText } = render(FamilyDetailsPage, {
            props: props
        });
        expect(getByText('Test Member')).toBeDefined();
    });

    it('should navigate to add member page when add member button is clicked', () => {
        const { getByText } = render(FamilyDetailsPage, {
            props: props
        });
        const addMemberButton = getByText('Add member');
        addMemberButton.click();
        expect(goto).toHaveBeenCalledWith('/family/1/member/add');
    });

    it('should delete family member', async () => {
        const { getByText, getAllByText  } = render(FamilyDetailsPage, {
            props: props
        });
        const deleteButtons = getAllByText('Delete');
       
        fireEvent.click(deleteButtons[0]);
        await waitFor(() => {
            expect(getByText('Delete member')).toBeDefined();
        });
    });
});
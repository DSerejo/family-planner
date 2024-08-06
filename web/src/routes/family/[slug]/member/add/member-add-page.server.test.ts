import { actions } from './+page.server';
import { familyService, familyLocalsService } from '$lib/family/family.service';
import { redirect } from '@sveltejs/kit';
import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('$lib/family/family.service', () => ({
    familyService: {
        addMember: vi.fn()
    },
    familyLocalsService: {
        addMember: vi.fn()
    }
}));
vi.mock('@sveltejs/kit');

describe('actions', () => {
    describe('default', () => {
        let event: any;

        beforeEach(() => {
            event = {
                request: {
                    formData: vi.fn().mockResolvedValue(new Map([
                        ['name', 'John Doe'],
                        ['email', 'john.doe@example.com']
                    ]))
                },
                params: { slug: 'family-id' },
                locals: {}
            };
        });
        it('should add a new member without email', async () => {
            const newMember = { id: 'new-member-id', name: 'John Doe' };
            vi.mocked(familyService.addMember).mockResolvedValue(newMember);
            vi.mocked(familyLocalsService.addMember).mockResolvedValue();
            event.request.formData = vi.fn().mockResolvedValue(new Map([
                ['name', 'John Doe']
            ]));
            await expect(actions.default(event)).rejects.toThrow(redirect(303, '/family/family-id'));

            expect(familyService.addMember).toHaveBeenCalledWith('family-id', { name: 'John Doe' });
            expect(familyLocalsService.addMember).toHaveBeenCalledWith(event, 'family-id', newMember);
        });
        it('should add a new member and redirect', async () => {
            const newMember = { id: 'new-member-id', name: 'John Doe', email: 'john.doe@example.com' };
            vi.mocked(familyService.addMember).mockResolvedValue(newMember);
            vi.mocked(familyLocalsService.addMember).mockResolvedValue();
            await expect(actions.default(event)).rejects.toThrow(redirect(303, '/family/family-id'));

            expect(familyService.addMember).toHaveBeenCalledWith('family-id', { name: 'John Doe', email: 'john.doe@example.com' });
            expect(familyLocalsService.addMember).toHaveBeenCalledWith(event, 'family-id', newMember);
        });

        it('should handle errors and set event.locals.error', async () => {
            const error = { status: 400, message: { detail: 'Invalid data' } };
            vi.mocked(familyService.addMember).mockRejectedValue(error);

            await actions.default(event);

            expect(event.locals.error).toBe('Invalid data');
        });

        it('should handle 422 errors and set event.locals.error', async () => {
            const error = { status: 422, message: { detail: [{ msg: 'Validation error' }] } };
            vi.mocked(familyService.addMember).mockRejectedValue(error);

            await actions.default(event);

            expect(event.locals.error).toBe('Validation error');
        });

        it('should handle unknown errors and set a default error message', async () => {
            const error = { status: 500 };
            vi.mocked(familyService.addMember).mockRejectedValue(error);

            await actions.default(event);

            expect(event.locals.error).toBe('Error adding member');
        });
    });
});

import { load } from './+layout.server';
import { describe, it, expect, vi } from 'vitest';

describe('load', () => {
  it('should return googleSession from locals', async () => {
    const event = {
      locals: { auth: vi.fn().mockResolvedValue({ user: 'testUser' }) }
    };

    const result = await load(event);

    expect(result).toEqual({
      googleSession: { user: 'testUser' }
    });
  });
});
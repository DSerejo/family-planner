import { GET } from './+server';
import { describe, it, expect, vi } from 'vitest';
import { error, json } from '@sveltejs/kit';

vi.mock('@sveltejs/kit', () => ({
    json: vi.fn(),
    error: vi.fn()
  }));

describe('GET', () => {
  it('should return 401 if no session', async () => {
    const locals = { auth: vi.fn().mockResolvedValue(null) };
    const url = new URL('http://localhost');
    const cookies = {};
    try {
        await GET({ url, locals, cookies });
    } catch (e) {
        expect(error).toHaveBeenCalledWith(401, 'Forbidden');
    }
  });

  it('should return user data if session exists', async () => {
    const session = { user: { name: 'John Doe' } };
    const locals = { auth: vi.fn().mockResolvedValue(session) };
    const url = new URL('http://localhost');
    const cookies = {};
    await GET({ url, locals, cookies });
    expect(json).toHaveBeenCalledWith({
      success: true,
      authenticatedUser: session.user
    });
  });
});
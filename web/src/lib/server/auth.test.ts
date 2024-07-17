import { AuthHandle } from './auth';
import { describe, it, expect, vi } from 'vitest';

describe('AuthHandle', () => {
  it('should set a unique requestId and call resolve', async () => {
    const event: any = {
      locals: {},
      cookies: { getAll: vi.fn().mockReturnValue([]) }
    };
    const resolve = vi.fn();

    await AuthHandle({ event, resolve });

    expect(event.locals.requestId).toBeDefined();
    expect(event.locals.requestId).toHaveLength(7);
    expect(resolve).toHaveBeenCalledWith(event);
  });
});
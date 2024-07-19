import { AuthHandle } from './auth';
import { describe, it, expect, vi, type Mock } from 'vitest';
import { api } from '../api';

vi.mock('../api', () => ({
  api: {
    post: vi.fn()
  }
}));
const POST = api.post as unknown as Mock

describe('AuthHandle', () => {
  it('should not create a session if there is no googleSession', async () => {
    const mockEvent: any = {
      locals: {
        auth: vi.fn().mockResolvedValue(undefined),
        session: undefined
      },
      cookies: {
        get: vi.fn().mockReturnValue(undefined),
        delete: vi.fn()
      }
    };
    const mockResolve = vi.fn();

    AuthHandle({ event: mockEvent, resolve: mockResolve });
    await mockEvent.locals.session()
    expect(mockEvent.locals.auth).toHaveBeenCalled();
    expect(await mockEvent.locals.session()).toBeUndefined();
    expect(mockResolve).toHaveBeenCalledWith(mockEvent);
  });

  it('should create a new session if the user is logged in to google but does not have a session in the api', async () => {
    const mockEvent: any = {
      locals: {
        auth: vi.fn().mockResolvedValue({ user: { email: 'testUser' } }),
        session: undefined
      },
      cookies: {
        set: vi.fn(),
        get: vi.fn().mockReturnValue(undefined)
      }
    };
    const mockResolve = vi.fn();
   

    POST.mockResolvedValueOnce({ token: 'testToken' });

    AuthHandle({ event: mockEvent, resolve: mockResolve });
    await mockEvent.locals.session()
    expect(mockEvent.locals.auth).toHaveBeenCalled();
    expect(POST).toHaveBeenCalledWith('/session', { email: 'testUser' });
    expect(mockEvent.cookies.set).toHaveBeenCalledWith('session', expect.any(String), expect.any(Object));
    expect(mockResolve).toHaveBeenCalledWith(mockEvent);
  });

  it('if the user is not found, create a user and then create a session', async () => {
    const googleSession = {user: { email: 'testUser', name: 'testUser' }};
    const mockEvent: any = {
      locals: {
        auth: vi.fn().mockResolvedValue(googleSession),
        session: null
      },
      cookies: {
        set: vi.fn(),
        get: vi.fn().mockReturnValue(undefined)
      }
    };
    const mockResolve = vi.fn();

    POST
      .mockRejectedValueOnce({ status: 401 })
      .mockResolvedValueOnce({ email: 'userData' })
      .mockResolvedValueOnce({ token: 'sessionData' });

    AuthHandle({ event: mockEvent, resolve: mockResolve });
    await mockEvent.locals.session()
    expect(mockEvent.locals.auth).toHaveBeenCalled();
    expect(POST).toHaveBeenCalledWith('/session', { email: 'testUser', name: 'testUser' });
    expect(POST).toHaveBeenCalledWith('/user', { email: 'testUser', name: 'testUser' });
    expect(POST).toHaveBeenCalledWith('/session', { email: 'testUser', name: 'testUser' });
    expect(mockEvent.cookies.set).toHaveBeenCalledWith('session', expect.any(String), expect.any(Object));
    expect(mockResolve).toHaveBeenCalledWith(mockEvent);
  });

  it('should not create a new session if cookie is present', async () => {
    const mockEvent: any = {
      locals: {
        auth: vi.fn().mockResolvedValue({ user: { email: 'testUser' } }),
        session: null
      },
      cookies: {
        get: vi.fn().mockReturnValue(Buffer.from(JSON.stringify({ token: 'sessionData' })).toString('base64'))
      }
    };
    const mockResolve = vi.fn();

    AuthHandle({ event: mockEvent, resolve: mockResolve });
    await mockEvent.locals.session()
    expect(mockEvent.locals.auth).toHaveBeenCalled();
    expect(mockResolve).toHaveBeenCalledWith(mockEvent);
  });
});
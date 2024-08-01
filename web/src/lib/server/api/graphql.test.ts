import { describe, it, expect, vi, beforeEach, type Mock } from 'vitest';
import { graphql } from './graphql'
import { api } from './api'

vi.mock('./api', () => ({
   api: {
    post: vi.fn()
   }
}))

describe('graphql', () => {
   

    it('should return make a query using graphql', async () => {
        (api.post as Mock).mockResolvedValue({ data: { user: { id: 1, email: 'test@example.com', name: 'Test User' } } })
        const query = `
            query GetUser($email: String!) {
                user(email: $email) {
                    id
                    email
                    name
                }
            }
        `   
        const variables = { email: 'test@example.com' }
        const response = await graphql(query, variables)
        expect(response).toEqual({ data: { user: { id: 1, email: 'test@example.com', name: 'Test User' } } })
    })
})
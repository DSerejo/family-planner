import { api } from './api'

export const graphql = async <R = unknown>(query: string, variables: Record<string, any>) => {
    try {
        return await api.post<{data: R}>('/graphql', { query, variables })
    } catch (error: any) {
        if(error.status === 401) {
            throw Error("Unauthorized")
        }
        return null
    }
}
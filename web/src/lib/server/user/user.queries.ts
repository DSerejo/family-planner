import { graphql } from "$lib/server/api/graphql"
import type { User } from "$lib/user/user.interface"

export const getUserWithFamilies = (email: string) => {
    return graphql<{user: User}>(`query GetUserWithFamilies($email: String!) {
        user(email: $email) {
            id
            email
            name
            families {
                id
                name
            }
        }
    }`, { email })
}
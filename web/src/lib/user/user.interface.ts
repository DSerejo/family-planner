import type { Family } from "$lib/family/family.interface"

export interface User {
    id: number
    email: string
    name: string
    families?: Family[]
}
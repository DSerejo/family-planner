export interface Family {
    id: string
    name: string
    members?: FamilyMember[]
}

export interface FamilyMember {
    id: string
    email?: string
    name: string
}

export interface FamilyMemberCreate {
    email?: string
    name?: string
}
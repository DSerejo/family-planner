
export const familyQuery = `
    query Family($familyId: ID!) {
        family(id: $familyId) {
            id
            name,
            members {
                id
                name,
                email
            }
        }
    }
`
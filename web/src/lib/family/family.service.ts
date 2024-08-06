import { api, type Api } from "$lib/server/api/api"
import type { RequestEvent } from "@sveltejs/kit"
import type { Family, FamilyMember, FamilyMemberCreate } from "./family.interface"
import { graphql } from "$lib/server/api/graphql"
import { familyQuery } from "./family.queries"

export class FamilyService {
    private api: Api
    private graphql: typeof graphql

    constructor() {
        this.api = api
        this.graphql = graphql
    }

    async addMember(familyId: string, member: FamilyMemberCreate): Promise<FamilyMember> {
        return this.api.post<FamilyMember>(`/family/${familyId}/member`, member)
    }

    async getFamily(familyId: string): Promise<Family | undefined> {
        const result = await this.graphql<{family: Family}>(familyQuery, { familyId })
        return result?.data?.family
    }

    async deleteFamilyMember(familyId: string, memberId: string) {
        return this.api.delete(`/family/${familyId}/member/${memberId}`)
    }

}

export class FamilyLocalsService {

    addMember<T extends RequestEvent>(event: T, familyId: string, member: FamilyMember) {
        this.init(event)
        event.locals.mappedFamilies![familyId]?.members?.push(member)
    }

    init<T extends RequestEvent>(event: T) {
        event.locals.mappedFamilies = event.locals.mappedFamilies || {}
        if (Object.keys(event.locals.mappedFamilies!).length === 0) {
            this.mapFamilies(event, event.locals.families || [])
        }
    }

    getFamily<T extends RequestEvent>(event: T, familyId: string): Family | undefined {
        this.init(event)
        return event.locals.mappedFamilies![familyId]
    }

    addFamily<T extends RequestEvent>(event: T, family: Family) {
        this.init(event)
        if(!event.locals.mappedFamilies![family.id]) {
            event.locals.mappedFamilies![family.id] = family
            event.locals.families = [...(event.locals.families || []), family]
        }
    }

    mapFamilies<T extends RequestEvent>(event: T, families: Family[]) {
        event.locals.mappedFamilies = families.reduce((acc: Record<string, Family>, family) => {
            acc[family.id] = family
            return acc
        }, {})
    }

}

export const familyLocalsService = new FamilyLocalsService()
export const familyService = new FamilyService()
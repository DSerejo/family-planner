
import { describe, it, expect, vi } from "vitest"
import { render, fireEvent } from '@testing-library/svelte';
import FamilyPage from "./+page.svelte";
import * as navigation from "$app/navigation";

vi.mock('$app/navigation', () => ({
	goto: vi.fn()
}));

describe("Family page", () => {

    it("should render", () => {
        const { getByText } = render(FamilyPage, {
            data: {
                session: {
                    user: {
                        email: "test@test.com"
                    }
                },
                googleSession: {
                    user: {
                        email: "test@test.com"
                    }
                }
            }
        });
        expect(getByText("Family")).toBeDefined();
    })

    it("should redirect to login if user is not logged in", () => {
        render(FamilyPage, {
            data: {
                session: null,
                googleSession: null
            }
        });
        expect(navigation.goto).toHaveBeenCalledWith('/');
    })

    it("should show list of families for the user to select if user has any family", () => {
        const { getByText } = render(FamilyPage, {
            data: {
                families: [{id: '1', name: "Family 1"}, {id: '2', name: "Family 2"}],
                session: {
                    user: {
                        email: "test@test.com"
                    }
                },
                googleSession: {
                    user: {
                        email: "test@test.com"
                    }
                }
            }
        });
        expect(getByText("Family 1")).toBeDefined();
        expect(getByText("Family 2")).toBeDefined();
    })

    it("should show create family if user does not have any family", () => {
        const { getByText } = render(FamilyPage, {
            data: {
                family: [],
                session: {
                    user: {
                        email: "test@test.com"
                    }
                },
                googleSession: {
                    user: {
                        email: "test@test.com"
                    }
                }
            }
        });
        expect(getByText("Create")).toBeDefined();
    })
})
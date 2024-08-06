
import { describe, it, expect, vi } from "vitest"
import { render, fireEvent, waitFor } from '@testing-library/svelte';
import FamilyPage from "./+page.svelte";
import * as navigation from "$app/navigation";

vi.mock('$app/navigation', () => ({
	goto: vi.fn(),
    invalidateAll: vi.fn()
}));
global.fetch = vi.fn()
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
        expect(getByText("My Families")).toBeDefined();
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
                families: [],
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

    it("should popup a modal when user clicks on delete family", async () => {
        const { getAllByText, getByText } = render(FamilyPage, {
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
        const deleteButton = getAllByText("Delete");
        fireEvent.click(deleteButton[0]);
        await waitFor(() => {
            expect(getByText("Are you sure you want to delete this family?")).toBeDefined();
        })
    })

    it("should delete family and reload the page", async () => {
        const { findByText, getByText, getAllByText } = render(FamilyPage, {
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
        const deleteButton = getAllByText("Delete");
        fireEvent.click(deleteButton[0]);
        await findByText("Are you sure you want to delete this family?");
        const confirmButton = getAllByText("Delete");
        fireEvent.click(confirmButton[2]);
        await waitFor(() => {
            expect(getByText("Family deleted")).toBeDefined();
        })
        expect(navigation.invalidateAll).toHaveBeenCalled();
    })
})
<script lang="ts">
    import type {PageData} from "./$types"
    import {signIn} from "@auth/sveltekit/client"
    import {signOut} from "$lib/auth/auth.client"
	import { goto } from "$app/navigation";

    const goToFamily = () => {
        goto("/family")
    }
    export let data: PageData;
  </script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

<p>
    {#if data.googleSession}
        <span>
            <small>Signed in as</small><br/>
            <strong>{data.googleSession.user?.name ?? "User"}</strong>
        </span>
        <button on:click={() => signOut()} class="button">Sign out</button>
        <button on:click={() => goToFamily()} class="button">Family</button>
    {:else}
        <span>You are not signed in</span>
        <button on:click={() => signIn("google")}>
            Sign In with Google
        </button>
    {/if}
</p>

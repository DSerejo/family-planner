<script lang="ts">
	import BottomAppBar, { Section, AutoAdjust } from '@smui-extra/bottom-app-bar';
	import IconButton from '@smui/icon-button';

    import "../theme/all.scss"
	let bottomAppBar: BottomAppBar;
</script>

<div class="layout">
	<AutoAdjust {bottomAppBar} class="layout-content">
		<div class="app-content">
			<slot></slot>
		</div>
	</AutoAdjust>
    <BottomAppBar bind:this={bottomAppBar}>
        <Section class="section">
            <a href="/family">
                <IconButton class="material-symbols-outlined">diversity_3</IconButton>
            </a>
            <IconButton class="material-symbols-outlined">menu</IconButton>
            <IconButton class="material-symbols-outlined">menu</IconButton>
        </Section>
	</BottomAppBar>
</div>



<style lang="scss">
    $maxWidth: 600px;
	.layout {
		display: flex;
		flex-direction: column;
		width: 100vw;
		height: 100vh;
		:global(main){
            height: 100% !important;
        }
        a {
            color: inherit;
        }
        > :global(.smui-bottom-app-bar){
            position: fixed;
            bottom: 0;
            right: 0;
            max-width: $maxWidth;
        }
        @media screen and (min-width: 600px) {
            :global(.smui-bottom-app-bar){
                left: calc(50vw - $maxWidth / 2);
            }
        }
        :global(.smui-bottom-app-bar__section){
            display: flex;
            justify-content: space-between;
        }
	}
	.app-content {
		max-width: $maxWidth;
		width: 100%;
		margin: 0 auto;
		display: flex;
        min-height: 100%;
        box-sizing: border-box;
	}

	/* Hide everything above this component. */
	:global(app),
	:global(body),
	:global(html) {
		display: block !important;
		height: auto !important;
		width: auto !important;
		position: static !important;
	}
    :global(body){
        margin: 0 !important;   
    }
</style>

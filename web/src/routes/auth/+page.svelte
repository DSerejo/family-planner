<script>
	import { page } from '$app/stores';
	import { get } from 'svelte/store';
  import { onMount } from 'svelte';
  let data
	const pageStore = get(page);
	onMount(async () => {
		data = await fetch('http://localhost:6051')
			.then((response) => response.json())
			.then((d) => JSON.stringify(d))
			.catch((error) => console.error('error', error));
		console.log(data);
	});
</script>

<div>{data}</div>

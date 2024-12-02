<script>
	import { error } from '@sveltejs/kit';
	import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

	let urlEnabled = $props();
	let url = $state('');
</script>

<div class="w-full h-full flex justify-center items-center">
	<div class="flex-1 grid gap-1 place-items-center">
		<div class="font-semibold text-sm">
			PDF download URL
		</div>
		<input
			type="text"
			bind:value={url}
			placeholder="https://xyz.com/policy.pdf"
			class="w-64 sm:w-96 lg:w-11/12 px-4 py-2 h-min text-sm bg-neutral-800 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
		<button
			onclick={() => {dispatch('url', url)}}
			disabled={url == ''}
			class="px-4 py-2 h-min w-auto lg:w-3/5 rounded-md {url != '' ? 'text-white bg-blue-500 hover:bg-blue-600 cursor-pointer' : 'text-neutral-300 bg-neutral-800 cursor-not-allowed'} transition">
			Send URL
		</button>
	</div>
</div>
<script>
	import { createEventDispatcher } from "svelte";
	import File from "./File.svelte";
	import Url from "./Url.svelte";

	const dispatch = createEventDispatcher();
	
	let response = $state('');
	export const snapshot = {
		capture: () => apiKey,
		restore: (value) => apiKey = value
	}
	let apiKey = $state('')
	let { responseJson = '' } = $props();
	let requestInProgress = $state(false);

	async function fetchFromAPI(type, value) {
		if (requestInProgress) {
			return
		}
		try {
			requestInProgress = true
			dispatch('setOverlay', true)
			if (type == "URL") {
				let queryParams = `?url=${value}`
				if (apiKey != '') {
					queryParams += `&api_key=${apiKey}`
				}
				response = await fetch(`http://127.0.0.1:8000/url${queryParams}`);
			} else {
				let formData = new FormData();
				formData.append('file', value);
				formData.append('api_key', apiKey)
				response = await fetch(
					'http://127.0.0.1:8000/file',
					{
						method: 'POST',
						body: formData
					}
				)
			}
			responseJson = await response.json();
		} catch (err) {
			responseJson = {status: "error", detail: err}
		}
		requestInProgress = false;
		dispatch('setOverlay', false);
	}

</script>

<div class="w-4/5 h-4/5 bg-[#141416] border rounded-md text-gray-200">
	{#if responseJson == ''}
		<div class="w-full h-full grid grid-rows-[2fr_4fr] sm:grid-rows-[3fr_5fr] p-4 gap-4 place-items-center">
			<div class="grid gap-4 font-display">
				<div class="font-bold lg:font-extrabold text-lg sm:text-xl md:text-3xl lg:text-5xl text-center font-cursive">
					Simplify <span class="font-display text-[#141416] stroked">POLICIES</span>, Amplify <span class="font-display text-[#141416] stroked">UNDERSTANDING</span>
				</div>
				<div class="px-10 sm:px-16 text-base lg:text-lg font-light text-center">
					Harness the Power of AI to decode Privacy Policies, eliminating the tedious task of reading lengthy and complex PDFs
				</div>
			</div>
			<div class="h-full w-5/6 grid place-items-center">
				<div class="h-full w-full grid grid-rows-[2fr_1fr_2fr] lg:grid-rows-none lg:grid-cols-[2fr_1fr_2fr] place-items-center">
					<Url on:url={event => fetchFromAPI("URL", event.detail)}></Url>
					<div class="font-bold text-3xl">
						OR
					</div>
					<File on:file={event => fetchFromAPI("FILE", event.detail)}></File>
				</div>
				<div>
					<input
						type="text"
						bind:value={apiKey}
						placeholder="Gemini API KEY"
						class="w-64 sm:w-96 px-4 py-2 text-sm bg-neutral-800 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
				</div>
			</div>
		</div>
	{:else}
		<div class="w-full h-full p-4 grid grid-flow-row gap-4 place-items-center">
			{#if responseJson.status == "success"}
				<div class="font-semibold text-xl p-4">
					Analyze {responseJson.response.companyName != '' ? responseJson.response.companyName: ''} Privacy Policy
				</div>
				<div class="overflow-auto w-full h-96 border border-gray-300 flex flex-col">
					<div class="grid grid-cols-[minmax(300px,_3fr)_minmax(250px,_2fr)_minmax(250px,_2fr)_minmax(150px,_1fr)] sticky z-10">
							<div class="px-4 py-2 font-bold border bg-[#141416]">Data Collected</div>
							<div class="px-4 py-2 font-bold border bg-[#141416]">Purpose</div>
							<div class="px-4 py-2 font-bold border bg-[#141416]">Retention Period</div>
							<div class="px-4 py-2 font-bold border bg-[#141416]">Criticality</div>
					</div>
					{#each responseJson.response.dataPolicyPoints as policy}
							<div class="grid grid-cols-[minmax(300px,_3fr)_minmax(250px,_2fr)_minmax(250px,_2fr)_minmax(150px,_1fr)]">
									<div class="px-4 py-2 border">{policy.dataCollected}</div>
									<div class="px-4 py-2 border">{policy.purpose}</div>
									<div class="px-4 py-2 border">{policy.retentionPeriod}</div>
									<div class="px-4 py-2 border">{policy.criticality}</div>
							</div>
					{/each}
				</div>
			{:else}
				<div class="w-3/4 h-2/5 p-4 bg-red-300 rounded-md text-neutral-900">
					{responseJson.detail}
				</div>
			{/if}
			<button onclick={() => {responseJson=''}} class="px-4 py-2 h-min w-auto text-center rounded-md cursor-pointer text-white bg-blue-500 hover:bg-blue-600 transition">
				Reset
			</button>
		</div>
	{/if}
</div>

<style>
	.stroked {
		-webkit-text-stroke: 1px #d4d4d8;
		paint-order: stroke fill;
	}
</style>
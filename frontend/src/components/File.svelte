<script>
	import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

	let file = null;

	function shortenFileName(name) {
    if (name.length > 20) {
      const start = name.slice(0, 10);
      const end = name.slice(-6);
      return `${start}...${end}`;
    }
    return name;
  }

	function handleFileUpload(event) {
		file = event.target.files[0];
	}

	function discardFile() {
		file = null;
		document.getElementById('file-upload').value = '';
	}
</script>

<div class="w-full h-full flex justify-center items-center">
	<input 
		type="file"
		accept="application/pdf"
		on:change={handleFileUpload}
		id="file-upload"
		class="hidden border border-gray-300 rounded-md focus:outline-none"/>

	<div class="flex-1 grid grid-flow-row gap-1 place-items-center">
		{#if file}
			<div class="text-sm">
				<span class="font-semibold">File:</span> {shortenFileName(file.name)}
			</div>
			<div class="grid grid-flow-col lg:grid-flow-row gap-1">
				<button
					on:click={() => {dispatch('file', file)}}
					class="px-4 py-2 h-min w-auto bg-blue-500 text-white rounded-md cursor-pointer hover:bg-blue-600 transition">
					Upload File
				</button>
				<button 
					on:click={discardFile}
					class="px-4 py-2 h-min w-auto bg-red-500 text-white rounded-md cursor-pointer hover:bg-red-600 transition">
					Discard
				</button>
			</div>	
		{:else}
			<div class="font-semibold text-sm">
				No File Selected !!
			</div>
			<label
				for="file-upload"
				class="px-4 py-2 h-min w-auto lg:w-4/5 text-center rounded-md cursor-pointer text-white bg-blue-500 hover:bg-blue-600 transition">
				Choose File
			</label>
		{/if}
	</div>
</div>
<script>
	import "../app.css";
	import Header from "../components/Header.svelte";
	import Card from "../components/Card.svelte";
	let overlay = $state(false);
</script>

<div class="bg-[#141416] bg-[radial-gradient(at_top_left,_rgba(150,150,150,0.1),_transparent)]">
	<div class="flex flex-col w-screen h-svh font-display ">
		<Header></Header>
		{#if overlay}
			<div class="w-full h-full absolute z-10 flex justify-center items-center overflow-hidden">
				<div class="flex justify-center items-center w-2/5 h-2/5 p-4 rounded-md border border-white bg-[#141416] font-semibold text-xl text-center text-neutral-300">
					Please wait while we summon the AI to process your request...
				</div>
			</div>
		{/if}
		<div>
			<div class="w-screen h-svh bg-[linear-gradient(to_right,#80808030_1px,transparent_1px),linear-gradient(to_bottom,#80808030_1px,transparent_1px)] bg-[size:24px_24px] flex-1 flex {overlay ? 'blur-sm': ''} justify-center items-center">
				<Card on:setOverlay={event => {overlay = event.detail}}></Card>
			</div>
		</div>
	</div>
</div>
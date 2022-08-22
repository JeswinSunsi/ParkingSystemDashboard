<template>
	<div class="wrapper">
		<div class="section">
			<h1>GENERAL</h1>
			<h3 @click="changeActive('/')" :class="{ colored: active == '/' }">Add Vehicle</h3>
			<h3 @click="changeActive('delete')" :class="{ colored: active == 'delete' }">Remove Vehicle</h3>
			<h3 @click="changeActive('alldetails')" :class="{ colored: active == 'alldetails' }">Show Vehicle Data</h3>
		</div>
		<div class="section">
			<h1>SETTINGS</h1>
			<h3 @click="changeActive('changegrid')" :class="{ colored: active == 'changegrid' }">Change Grid</h3>
			<h3>Add N/A Spot</h3>
			<h3>Show All Records</h3>
		</div>
		<div class="section">
			<h1>TESTING</h1>
			<h3>Add Random</h3>
			<h3 @click="clearAll" :class="{ colored: active == 'clearall' }">Clear All</h3>
			<h3>Refresh DB</h3>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useMainStore } from "../stores/useMainStore.js";

const main = useMainStore();
const { subscribeToChange } = main;
const router = useRouter();
const active = ref("/");

function changeActive(value) {
	active.value = value;
	router.push(value);
}

async function clearAll() {
	try {
		await axios.get(`https://cwapi.jeswinsunsi.repl.co/v1/clearall`);
		subscribeToChange();
	} catch (error) {
		console.error(error);
	}
}
</script>

<style scoped>
.wrapper {
	min-width: 10rem;
	height: 100vh;
	background-color: #252525;
	display: flex;
	padding: 5rem 0rem 5rem 1.25rem;
	align-items: flex-start;
	flex-direction: column;
	justify-content: space-around;
	font-family: Poppins;
	color: #ffffff;
}

h1 {
	font-size: 0.75rem;
	font-weight: 600;
	margin-bottom: 1.4rem;
}

h3 {
	font-size: 0.75rem;
	font-weight: 300;
	margin-bottom: 1rem;
	cursor: pointer;
}

.colored {
	color: #f8a605;
}
</style>

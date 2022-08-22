<template>
	<div class="wrapper">
		<div class="titlebar">Add New Vehicle To Lot</div>
		<div class="data-fields">
			<div class="flex-row">
				<div class="input">
					<div class="text">PLATE NUM</div>
					<input type="text" class="input" v-model="id" />
				</div>
				<div class="input">
					<div class="text">VEHICLE COLOR</div>
					<input type="text" class="input" v-model="color" />
				</div>
			</div>
			<div class="flex-row">
				<div class="input">
					<div class="text">VEHICLE MODEL</div>
					<input type="text" class="input" v-model="name" />
				</div>
				<div class="input">
					<div class="text">VEHICLE TYPE</div>
					<input type="text" class="input" v-model="vehicletype" />
				</div>
			</div>
			<div class="flex-row">
				<div class="input">
					<div class="text">DRIVER EMAIL</div>
					<input type="text" class="input" v-model="email" />
				</div>
				<div class="input">
					<div class="text">TIMESTAMP</div>
					<input type="text" class="input" placeholder="Auto-Generated" />
				</div>
			</div>
			<div class="confirm" @click="addNewCar">CONFIRM</div>
		</div>
	</div>
</template>

<script setup>
import axios from "axios";
import { ref } from "vue";
import { useMainStore } from "../../stores/useMainStore.js";
const main = useMainStore();

const { subscribeToChange } = main;

const email = ref("");
const name = ref("");
const color = ref("");
const vehicletype = ref("");
const id = ref("");

async function addNewCar() {
	try {
		const data = await axios.get(`https://cwapi.jeswinsunsi.repl.co/v1/getdetails/${id.value}`);
		console.log(data);
		subscribeToChange();
		email.value = data.data.email;
		name.value = data.data.name;
		color.value = data.data.color;
		vehicletype.value = data.data.type;
	} catch (error) {
		console.error(error);
	}
}
</script>

<style scoped>
.wrapper {
	width: 100%;
	font-family: Poppins;
}
.titlebar {
	width: 100%;
	height: 2.5rem;
	background-color: #f8a605;
	display: flex;
	align-items: center;
	padding-left: 1.2rem;
	font-weight: 600;
	color: #ffffff;
	margin-bottom: 2rem;
}

.text {
	font-size: 0.7rem;
	margin-bottom: 0.2rem;
}

.flex-row {
	width: 100%;
	display: flex;
	justify-content: space-between;
	margin-bottom: 1.75rem;
}

.input {
	width: 80%;
	font-size: 1rem;
	font-weight: 500;
	padding: 0.2rem;
	color: #2a2a2a;
}

textarea:focus,
input:focus {
	outline: none;
}

.confirm {
	height: max-content;
	width: max-content;
	padding: 0.6rem 1.5rem;
	background-color: #8448f4;
	color: #fff;
	font-size: 0.8rem;
	font-weight: 500;
	border-radius: 0.1rem;
	display: flex;
	justify-content: center;
	align-items: center;
	cursor: pointer;
}

.confirm:hover {
	transform: translateY(1px);
}
</style>

<template>
	<div class="container">
		<span class="group-one">
			<div class="entrance"></div>
			<div class="parking-lot">
				<div class="row" v-for="vehicles in rows" :key="vehicles">
					<div class="flex-wrapper" v-if="vehicles.bikes">
						<div class="vertical-wrapper" v-for="spot in 2" :key="spot">
							<div class="car reserved">R</div>
						</div>
						<div class="vehicle-wrapper" v-for="(vehicle, index) in vehicles.bikes" :key="vehicle">
							<div class="vertical-wrapper">
								<div class="vehicle tooltip" :class="{ vacant: vehicle[0] }">
									<span class="tooltiptext">{{ vehicle[0] ? vehicle[0] : "vacant" }} - A{{ index }}</span>
								</div>
								<div class="horizontal-divider" style="background-color: #ffffff"></div>
								<div class="vehicle tooltip" :class="{ vacant: vehicle[1] }">
									<span class="tooltiptext">{{ vehicle[0] ? vehicle[1] : "vacant" }} - A{{ index }}</span>
								</div>
							</div>
							<div class="vertical-divider" style="background-color: #ffffff"></div>
						</div>
					</div>

					<div class="vehicle-wrapper tooltip" v-for="(vehicle, index) in vehicles.cars" :key="vehicle">
						<span class="tooltiptext">{{ vehicle[0] ? vehicle : "vacant" }} - B{{ index }}</span>
						<div class="vertical-wrapper">
							<div class="car" :class="{ vacant: vehicle[0] }"></div>
						</div>
						<div class="vertical-divider" style="background-color: #ffffff"></div>
					</div>
					<div class="vehicle-wrapper tooltip" v-for="(vehicle, index) in vehicles.trucks" :key="vehicle">
						<span class="tooltiptext">{{ vehicle[0] ? vehicle : "vacant" }} - C{{ index }}</span>
						<div class="vertical-wrapper">
							<div class="vehicle" :class="{ vacant: vehicle[0] }" style="min-width: 2.5rem" v-if="vehicle != barrier"></div>
							<div class="horizontal-divider" :class="{ occupiedTruck: !vehicle[0], notOccupied: vehicle[0] }" style="min-width: 2.5rem" v-if="vehicle != barrier"></div>
							<div class="vehicle" :class="{ vacant: vehicle[1] }" v-if="vehicle != barrier"></div>
						</div>
						<div class="vertical-divider" v-if="vehicle == barrier"></div>
					</div>
				</div>
			</div>
		</span>
		<div class="legends">
			<div class="legend">
				<h3>vacant</h3>
				<div class="color-box" style="background-color: #7dd75f"></div>
			</div>
			<div class="legend">
				<h3>occupied</h3>
				<div class="color-box" style="background-color: #fe3f51"></div>
			</div>
			<div class="legend">
				<h3>unavailable</h3>
				<div class="color-box" style="background-color: #e2e2e2"></div>
			</div>
			<div class="legend">
				<h3>entrance</h3>
				<div class="color-box" style="background-color: #1f88f0"></div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "axios";
import { useMainStore } from "../stores/useMainStore.js";
import { storeToRefs } from "pinia";

const main = useMainStore();

const { hasChanged } = storeToRefs(main);

const rows = ref([]);

const barrier = ref("barrier");

async function getData() {
	try {
		const response = await axios.get(`https://cwapi.jeswinsunsi.repl.co/v1/showall`);
		rows.value[0] = response.data.finalLot;
	} catch (error) {
		console.error(error);
	}
}
getData();

watch(hasChanged, () => {
	getData();
});
</script>

<style scoped>
.occupiedTruck {
	background-color: #7dd75f !important;
}

.notOccupied {
	background-color: #fe3f51;
}

.tooltip .tooltiptext {
	visibility: hidden;
	width: max-content;
	background-color: rgb(31, 31, 31);
	color: #fff;
	text-align: center;
	border-radius: 6px;
	padding: 0.5rem 1rem;
	font-family: Poppins;
	font-size: 0.9rem;
	position: absolute;
	z-index: 1;
	top: -2.2rem;
	right: -100%;
}

.tooltip {
	position: relative;
}

.tooltip:hover .tooltiptext {
	visibility: visible;
}

.container {
	display: flex;
	flex-direction: row;
	padding: 2rem 0rem;
	justify-content: space-between;
}

.group-one {
	display: flex;
	justify-content: start;
}
.entrance {
	background-color: #1f88f0;
	height: 2.4rem;
	min-width: 2.4rem;
	margin-right: 0.2rem;
}

.lot {
	display: flex;
	flex-direction: column;
}

.row {
	display: flex;
	flex-wrap: wrap;
}

.vehicle-wrapper {
	display: flex;
	margin-bottom: 0.2rem;
}

.vertical-wrapper {
	display: flex;
	flex-direction: column;
}

.vehicle {
	height: 1.15rem;
	min-width: 2.4rem;
	background-color: #7dd75f;
}

.car {
	height: 2.3rem;
	min-width: 2.4rem;
	background-color: #7dd75f;
}

.horizontal-divider {
	min-height: 0.1rem;
	width: 2.4rem;
}

.vertical-divider {
	height: 2.4rem;
	width: 0.2rem;
}

.flex-wrapper {
	display: flex;
}

.vacant {
	background-color: #fe3f51;
}

.occupied {
	background-color: #7dd75f !important;
}

.reserved {
	background-color: #7dd75f !important;
	margin-right: 0.2rem;
	display: flex;
	justify-content: center;
	align-items: center;
	font-family: Poppins;
	color: #ffffff;
	font-size: 1.2rem;
}

.legends {
	display: flex;
	flex-direction: column;
	margin-left: 2rem;
	align-items: flex-end;
}

.color-box {
	height: 1.4rem;
	margin-left: 0.2rem;
	width: 1.4rem;
}

.legend {
	display: flex;
	margin-bottom: 0.3rem;
	align-items: center;
	font-family: Poppins;
	font-weight: 400;
	color: #696969;
	font-size: 0.7rem;
}
</style>

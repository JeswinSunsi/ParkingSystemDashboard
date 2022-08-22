import { defineStore } from "pinia";

export const useMainStore = defineStore("main", {
	state: () => ({
		hasChanged: false,
	}),
	actions: {
		subscribeToChange() {
			this.hasChanged = !this.hasChanged;
		},
	},
});

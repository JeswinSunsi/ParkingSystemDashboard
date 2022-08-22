import { createRouter, createWebHistory } from "vue-router";
import AddNew from "../components/Screens/AddNew.vue";
import DeleteOne from "../components/Screens/DeleteOne.vue";
import ChangeGrid from "../components/Screens/ChangeGrid.vue";
import AllDetails from "../components/Screens/AllRecords.vue";

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: "/",
			name: "home",
			component: AddNew,
		},
		{
			path: "/delete",
			name: "delete",
			component: DeleteOne,
		},
		{
			path: "/changegrid",
			name: "changegrid",
			component: ChangeGrid,
		},
		{
			path: "/alldetails",
			name: "alldetails",
			component: AllDetails,
		},
	],
});

export default router;

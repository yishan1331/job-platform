export interface INavigationRoute {
	name: string;
	displayName: string;
	meta: { icon: string };
	children?: INavigationRoute[];
}

export default {
	root: {
		name: "/",
		displayName: "navigationRoutes.home",
	},
	routes: [
		{
			name: "jobs",
			displayName: "sidebar.jobs",
			meta: {
				icon: "description",
			},
		},
	] as INavigationRoute[],
};

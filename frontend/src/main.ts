import { createApp } from "vue";
import i18n from "./i18n";
import { createVuestic } from "vuestic-ui";
import { createGtm } from "@gtm-support/vue-gtm";
import { useUserAuthStore } from "@/stores/user-auth";

import stores from "./stores";
import router from "./router";
import vuesticGlobalConfig from "./services/vuestic-ui/global-config";
import App from "./App.vue";

// import './scss/main.scss'; // 引入全局样式文件

const app = createApp(App);

app.use(stores);
app.use(router);
app.use(i18n);
app.use(createVuestic({ config: vuesticGlobalConfig }));

// 設置 i18n 語言
const authStore = useUserAuthStore();
i18n.global.locale.value = authStore.language || "gb";

if (import.meta.env.VITE_APP_GTM_ENABLED) {
	app.use(
		createGtm({
			id: import.meta.env.VITE_APP_GTM_KEY,
			debug: false,
			vueRouter: router,
		})
	);
}

app.mount("#app");

import { createPinia, setActivePinia } from 'pinia'

const pinia = createPinia()
export default setActivePinia(pinia)

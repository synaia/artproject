import { configureStore } from "@reduxjs/toolkit"

import providerReducer from './features/provider.feature.js';


const rootReducer = {
   provider: providerReducer,
}

const store = configureStore({
    reducer: rootReducer
})

export default store;
import { configureStore } from '@reduxjs/toolkit';
import patientsReducer from './patientsSlice';
import configReducer from './configSlice';

const store = configureStore({
  reducer: {
    patients: patientsReducer,
    config: configReducer
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;

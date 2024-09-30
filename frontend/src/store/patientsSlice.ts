import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

export interface Appointment {
  id: number;
  status: string;
  date_start: string;
  description: string;
}

export interface Patient {
  id: number;
  fullname: string;
  gender: string;
  birth_date: string;
  appointments: Appointment[];
}

interface PatientsState {
  patients: Patient[];
  loading: boolean;
  error: string | null;
}

const initialState: PatientsState = {
  patients: [],
  loading: false,
  error: null,
};

export const fetchPatients = createAsyncThunk(
  'patients/fetchPatients',
  async () => {
    const response = await axios.get(`${process.env.REACT_APP_API_URL}/patients/appointments`);
    return response.data;
  }
);

const patientsSlice = createSlice({
  name: 'patients',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchPatients.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPatients.fulfilled, (state, action) => {
        state.patients = action.payload;
        state.loading = false;
      })
      .addCase(fetchPatients.rejected, (state, action) => {
        state.error = action.error.message || 'Не получилось загрузить список пациентов';
        state.loading = false;
      });
  },
});

export default patientsSlice.reducer;
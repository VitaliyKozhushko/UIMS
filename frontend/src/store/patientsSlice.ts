import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface Patient {
  id: number;
  patientName: string;
  date: string;
  description: string;
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
    console.log(response.data)
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
        state.loading = false;
        state.patients = action.payload;
      })
      .addCase(fetchPatients.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Не получилось загрузить список пациентов';
      });
  },
});

export default patientsSlice.reducer;
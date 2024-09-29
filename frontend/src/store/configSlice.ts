import { createSlice, PayloadAction, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface ConfigState {
  offline: boolean;
}

const initialState: ConfigState = {
  offline: false
};

export const updateOffline = createAsyncThunk(
  'config/updateOffline',
  async (offline: boolean) => {
    const response = await axios.patch(`${process.env.REACT_APP_API_URL}/config/offline`, { offline });
    return response.data.offline;
  }
);

export const getOffline = createAsyncThunk('config/fetchOffline', async () => {
  const response = await axios.get(`${process.env.REACT_APP_API_URL}/config/offline`);
  return response.data.offline;
});

const configSlice = createSlice({
  name: 'config',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getOffline.fulfilled, (state, action: PayloadAction<boolean>) => {
        state.offline = action.payload;
      })
      .addCase(updateOffline.fulfilled, (state, action: PayloadAction<boolean>) => {
        state.offline = action.payload;
      });
  },
});

export default configSlice.reducer;
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface ConfigState {
  offline: boolean;
  resource: string;
}

interface UpdateOfflineParams {
  offline: boolean;
  resource: string;
}

const initialState: ConfigState = {
  offline: false,
  resource: ''
};

export const updateOffline = createAsyncThunk(
  'config/updateOffline',
  async ({ offline, resource }: UpdateOfflineParams) => {
    const response = await axios.patch(`${process.env.REACT_APP_API_URL}/resources/${resource}`, { offline });
    return response.data;
  }
);

export const getOffline = createAsyncThunk('config/getOffline', async (resource: string) => {
  const response = await axios.get(`${process.env.REACT_APP_API_URL}/resources/${resource}`);
  return response.data;
});

const configSlice = createSlice({
  name: 'config',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getOffline.fulfilled, (state, action) => {
        state.offline = action.payload.offline;
        state.resource = action.payload.type;
      })
      .addCase(updateOffline.fulfilled, (state, action) => {
        state.offline = action.payload.offline;
        state.resource = action.payload.type;
      });
  },
});

export default configSlice.reducer;
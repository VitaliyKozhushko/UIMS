import {createSlice, createAsyncThunk} from '@reduxjs/toolkit';
import axios from 'axios';

interface ConfigState {
  offline: boolean;
  resource: string;
  loadingConfig: boolean;
}

interface UpdateOfflineParams {
  offline: boolean;
  resource: string;
}

const initialState: ConfigState = {
  offline: false,
  resource: '',
  loadingConfig: false
};

export const updateOffline = createAsyncThunk(
  'config/updateOffline',
  async ({offline, resource}: UpdateOfflineParams) => {
    const response = await axios.patch(`${process.env.REACT_APP_API_URL}/resources/${resource}`, {offline});
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
      .addCase(getOffline.pending, (state) => {
        state.loadingConfig = true;
      })
      .addCase(updateOffline.pending, (state) => {
        state.loadingConfig = true;
      })
      .addCase(getOffline.fulfilled, (state, action) => {
        state.offline = action.payload.offline;
        state.resource = action.payload.type;
        state.loadingConfig = false;
      })
      .addCase(updateOffline.fulfilled, (state, action) => {
        state.offline = action.payload.offline;
        state.resource = action.payload.type;
        state.loadingConfig = false;
      })
      .addCase(getOffline.rejected, (state) => {
        state.loadingConfig = false;
      })
      .addCase(updateOffline.rejected, (state) => {
        state.loadingConfig = false;
      });
  },
});

export default configSlice.reducer;
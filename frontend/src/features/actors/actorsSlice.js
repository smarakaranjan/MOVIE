import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getActors } from "../../api/actorsApi";
import { getErrorMessage } from "../../utils/errorHandler";

export const fetchActors = createAsyncThunk(
  "actors/fetchActors",
  async (filters = {}, { rejectWithValue }) => {
    try {
      const data = await getActors(filters);
      return data;
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      return rejectWithValue(errorMessage);
    }
  }
);

const actorsSlice = createSlice({
  name: "actors",
  initialState: { 
    items: [], 
    status: "pending", 
    error: null, 
    filters: {},
    pagination: null,
  },
  reducers: {
    setFilters(state, action) {
      state.filters = action.payload;
    },
    clearFilters(state) {
      state.filters = {};
      state.items = [];
      state.pagination = null;
    },
    appendItems(state, action) {
      state.items = [...state.items, ...action.payload];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchActors.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchActors.fulfilled, (state, action) => {
        state.status = "succeeded";
        const results = action.payload.results ?? action.payload;
        const pagination = action.payload.pagination ?? null;
        
        // If we have existing items and pagination shows we're not on page 1, append
        if (state.items.length > 0 && pagination && pagination.current_page > 1) {
          state.items = [...state.items, ...results];
        } else {
          state.items = results;
        }
        state.pagination = pagination;
      })
      .addCase(fetchActors.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload;
      });
  },
});

export const { setFilters, clearFilters, appendItems } = actorsSlice.actions;
export default actorsSlice.reducer;

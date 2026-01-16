import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getMovies } from "../../api/moviesApi";
import { getErrorMessage } from "../../utils/errorHandler";

// -------------------- Async Thunk --------------------

export const fetchMovies = createAsyncThunk(
  "movies/fetchMovies",
  async (filters = {}, { rejectWithValue }) => {
    try {
      // Remove empty/null filters
      const cleanFilters = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v != null && v !== "")
      );

      const data = await getMovies(cleanFilters);
      return data;
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      return rejectWithValue(errorMessage);
    }
  }
);



// -------------------- Slice --------------------
const moviesSlice = createSlice({
  name: "movies",
  initialState: {
    items: [],
    status: "pending", // pending | loading | succeeded | failed
    error: null,
    filters: {}, // store current filters
    pagination: null, // store pagination metadata
  },
  reducers: {
    setFilters(state, action) {
      state.filters = action.payload;
    },
    clearFilters(state) {
      state.filters = {};
    },
  },
  extraReducers: (builder) => {
    // async thunk reducers
    builder
      .addCase(fetchMovies.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchMovies.fulfilled, (state, action) => {
        state.status = "succeeded";
        // if using DRF pagination, results might be in action.payload.results
        state.items = action.payload.results ?? action.payload;
        // store pagination metadata if available
        state.pagination = action.payload.pagination ?? null;
      })
      .addCase(fetchMovies.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload;
      });
  },
});

// Export actions for components to dispatch
export const { setFilters, clearFilters } = moviesSlice.actions;

// Export reducer for store
export default moviesSlice.reducer;

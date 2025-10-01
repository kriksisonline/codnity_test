import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

export const fetchStories = createAsyncThunk(
  "stories/fetchStories",
  async (_, { getState }) => {
    const state = getState().stories;

    const refreshRes = await fetch("http://localhost:5000/stories/refresh", {
      method: "GET",
    });
    if (!refreshRes.ok) throw new Error("Failed to refresh stories");
    const refreshData = await refreshRes.json();

    const shouldFetch =
      refreshData.updated > 0 || state.items.length === 0;

    if (shouldFetch) {
      const res = await fetch("http://localhost:5000/stories");
      if (!res.ok) throw new Error("Failed to fetch stories");
      return await res.json();
    }

    return state.items;
  }
);

const storiesSlice = createSlice({
  name: "stories",
  initialState: {
    items: [],
    status: "idle",
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchStories.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchStories.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload;
      })
      .addCase(fetchStories.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
      });
  },
});

export default storiesSlice.reducer;

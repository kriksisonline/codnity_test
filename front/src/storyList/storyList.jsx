import { useEffect, useState, useMemo } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchStories } from "../store/storySlice";
import StoryItem from "./storyItem";

export default function StoryList() {
  const dispatch = useDispatch();
  const { items: stories, status, error } = useSelector((state) => state.stories);

  const [sortOption, setSortOption] = useState("newest");
  const [searchQuery, setSearchQuery] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 15;

  useEffect(() => {
    if (status === "idle") {
      dispatch(fetchStories());
    }
  }, [status, dispatch]);

  const filteredStories = useMemo(() => {
    return stories.filter((s) =>
      s.title.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [stories, searchQuery]);

  const sortedStories = useMemo(() => {
    const sorted = [...filteredStories];
    switch (sortOption) {
      case "newest":
        return sorted.sort((a, b) => new Date(b.date_created) - new Date(a.date_created));
      case "oldest":
        return sorted.sort((a, b) => new Date(a.date_created) - new Date(b.date_created));
      case "highest":
        return sorted.sort((a, b) => b.points - a.points);
      case "lowest":
        return sorted.sort((a, b) => a.points - b.points);
      default:
        return sorted;
    }
  }, [filteredStories, sortOption]);

  const totalPages = Math.ceil(sortedStories.length / itemsPerPage);
  const paginatedStories = sortedStories.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <div className="section has-background-dark has-text-white" style={{ minHeight: "100vh" }}>
      <div className="container" style={{ maxWidth: "800px" }}>
        <h1 className="title has-text-centered has-text-white">Hacker News</h1>

        <div className="field is-grouped is-grouped-multiline is-justify-content-center mb-4">
          <div className="control is-expanded">
            <input
              className="input is-small"
              type="text"
              placeholder="Search by title..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setCurrentPage(1);
              }}
            />
          </div>

          <div className="control">
            <div className="select is-small">
              <select value={sortOption} onChange={(e) => setSortOption(e.target.value)}>
                <option value="newest">Newest</option>
                <option value="oldest">Oldest</option>
                <option value="highest">Highest points</option>
                <option value="lowest">Lowest points</option>
              </select>
            </div>
          </div>

          <div className="control">
            <button
              className="button is-info is-small"
              onClick={() => dispatch(fetchStories())}
            >
              Refresh
            </button>
          </div>
        </div>

        {status === "loading" && <p className="has-text-centered">Loading...</p>}
        {status === "failed" && (
          <p className="has-text-danger has-text-centered">{error}</p>
        )}
        {status === "succeeded" && (
          <>
            <ul>
              {paginatedStories.map((story, idx) => (
                <StoryItem key={idx} story={story} />
              ))}
            </ul>

            {totalPages > 1 && (
              <nav
                className="pagination is-centered is-small mt-3"
                role="navigation"
                aria-label="pagination"
              >
                <button
                  className="pagination-previous"
                  onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
                  disabled={currentPage === 1}
                >
                  ‹ Prev
                </button>
                <span className="pagination-link is-static mx-2">
                  Page {currentPage} / {totalPages}
                </span>
                <button
                  className="pagination-next"
                  onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
                  disabled={currentPage === totalPages}
                >
                  Next ›
                </button>
              </nav>
            )}
          </>
        )}
      </div>
    </div>
  );
}

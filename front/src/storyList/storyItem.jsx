import React, { memo } from "react";

function StoryItem({ story }) {
  return (
    <li className="box has-background-dark p-3 mb-2 is-size-7">
      <a
        href={story.link}
        target="_blank"
        rel="noopener noreferrer"
        className="has-text-info has-text-weight-semibold is-size-6"
      >
        {story.title}
      </a>
      <div className="has-text-grey-light">
        {story.points} points •{" "}
        {story.date_created ? new Date(story.date_created).toLocaleString() : "Unknown date"}
      </div>
    </li>
  );
}

export default memo(StoryItem);

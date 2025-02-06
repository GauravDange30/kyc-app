import React from "react";

const RetryButton = ({ onRetry }) => {
  return (
    <div>
      <button onClick={onRetry}>Retry Verification</button>
    </div>
  );
};

export default RetryButton;
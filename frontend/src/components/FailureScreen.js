import React from "react";

const FailureScreen = ({ errorMessage, onRetry }) => {
  return (
    <div>
      <h2>Verification Failed</h2>
      <p>{errorMessage}</p>
      <button onClick={onRetry}>Retry Verification</button>
    </div>
  );
};

export default FailureScreen;
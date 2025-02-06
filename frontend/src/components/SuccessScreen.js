import React from "react";

const SuccessScreen = ({ panData, bankData }) => {
  return (
    <div>
      <h2>Verification Successful!</h2>
      <p>PAN Details: {JSON.stringify(panData)}</p>
      <p>Bank Account Details: {JSON.stringify(bankData)}</p>
    </div>
  );
};

export default SuccessScreen;
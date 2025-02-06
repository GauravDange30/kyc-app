import React, { useState } from "react";
import axios from "axios";
import '../styles/VerificationModule.css';
import { useNavigate } from "react-router-dom";

const VerificationModule = () => {

  const navigate = useNavigate();
  // State variables
  const [panNumber, setPANNumber] = useState("");
  const [consent, setConsent] = useState(false);
  const [reason, setReason] = useState("");
  const [panMessage, setPanMessage] = useState(""); // PAN success/error message
  const [panError, setPanError] = useState(""); // PAN error message
  const [panVerified, setPanVerified] = useState(false);
  const [accountNumber, setAccountNumber] = useState("");
  const [ifscCode, setIfscCode] = useState("");
  const [bankMessage, setBankMessage] = useState(""); // Bank success/error message
  const [bankError, setBankError] = useState(""); // Bank error message

  // Reset function to clear all fields and errors
  const handleReset = () => {
    setPANNumber("");
    setConsent(false);
    setReason("");
    setPanMessage("");
    setPanError("");
    setPanVerified(false);
    setAccountNumber("");
    setIfscCode("");
    setBankMessage("");
    setBankError("");
  };

  // PAN verification function
  const handlePANSubmit = async () => {
    setPanMessage("");
    setPanError("");

    try {
      const payload = {
        pan: panNumber,
        consent: consent ? "Y" : "N",
        reason: reason.trim(),
      };

      const headers = {
        "x-client-id": process.env.REACT_APP_CLIENTID_API_KEY,
        "x-client-secret": process.env.REACT_APP_CLIENTSECRET_API_KEY,
        "x-product-instance-id": process.env.REACT_APP_PRODINSTANCE_API_KEY
      };

      const response = await axios.post(
        "http://localhost:8001/kyc_verification/api/verify/pan",
        payload,
        { headers }
      );

      if (response.status === 200 && response.data.verification === "SUCCESS") {
        setPanMessage(`Verification: ${response.data.verification}, Message: ${response.data.message}`);
        setPanVerified(true);
      } else {
        setPanError("PAN verification failed. Please try again.");
      }
    } catch (err) {
      if (err.response) {
        const { status, data } = err.response;
        if (status === 400 && data.error) {
          setPanError(`Error: ${data.error.code}, Detail: ${data.error.detail}`);
        } else {
          setPanError("An unexpected error occurred during PAN verification.");
        }
      } else {
        setPanError("Network error. Please try again.");
      }
    }
  };

  // Bank account verification function
  const handleBankAccountSubmit = async () => {
    setBankMessage("");
    setBankError("");

    const panStatus = panVerified ? "successful" : "failed_pan";

    const payload = {
      redirectionConfig: {
        redirectUrl: "https://www.google.com",
        timeout: 60,
      },
      additionalData: {
        acno: accountNumber,
        ifsc: ifscCode,
        pan_status: panStatus
      },
      
    };

    const headers = {
      "x-client-id": process.env.REACT_APP_CLIENTID_API_KEY,
      "x-client-secret": process.env.REACT_APP_CLIENTSECRET_API_KEY,
      "x-product-instance-id": process.env.REACT_APP_PRODINSTANCE_API_KEY_BANK
    };

    try {
      const response = await axios.post(
        "http://localhost:8001/kyc_verification/api/verify/ban/reverse",
        payload,
        { headers }
      );

      if (response.status === 200) {
        setBankMessage("Verification: SUCCESS, Message: BANK Is Verified");
      } else {
        setBankError("Bank account verification failed. Please try again.");
      }
    } catch (err) {
      setBankError("Network error. Please try again.");
    }
  };

  const goToAnalytics = () => {
    navigate("/analytics");
  };

  return (
    <div className="verification-container">
      <h2>PAN and Bank Account Verification</h2>

      {/* PAN Verification Section */}
      <div className="form-container">
        <h3>PAN Verification</h3>
        <input
          className="input-field"
          type="text"
          placeholder="Enter PAN Number"
          value={panNumber}
          onChange={(e) => setPANNumber(e.target.value)}
        />
        <br />
        <label>
          <input
            className="checkbox"
            type="checkbox"
            checked={consent}
            onChange={(e) => setConsent(e.target.checked)}
          />
          I give my consent
        </label>
        <br />
        <textarea
          className="input-field"
          placeholder="Enter reason"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
        />
        <br />
        {/* PAN Messages */}
        {panMessage && <p className="success-message">{panMessage}</p>}
        {panError && <p className="error-message">{panError}</p>}
      </div>

      {/* Bank Account Verification Section */}
      <div className="form-container">
        <h3>Bank Account Verification</h3>
        <input
          className="input-field"
          type="text"
          placeholder="Enter Bank Account Number"
          value={accountNumber}
          onChange={(e) => setAccountNumber(e.target.value)}
        />
        <br />
        <input
          className="input-field"
          type="text"
          placeholder="Enter IFSC Code"
          value={ifscCode}
          onChange={(e) => setIfscCode(e.target.value)}
        />
        <br />
        {/* Bank Messages */}
        {bankMessage && <p className="success-message">{bankMessage}</p>}
        {bankError && <p className="error-message">{bankError}</p>}
      </div>

      {/* Submit Button below the Bank Account Form */}
      <div className="submit-section">
        <button className="submit-btn" onClick={() => { handlePANSubmit(); handleBankAccountSubmit(); }}>Verify PAN and Bank Account</button>
      </div>

      {/* Reset & Analytics Buttons */}
      <div className="button-group">
        <button className="reset-btn" onClick={handleReset}>Reset</button>
        <button className="analytics-btn" onClick={goToAnalytics}>Go to Analytics</button>
      </div>
    </div>
  );
};

export default VerificationModule;

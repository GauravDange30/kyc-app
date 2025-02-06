import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import VerificationModule from "./components/VerificationModule"; // Updated import
import SuccessScreen from "./components/SuccessScreen";
import FailureScreen from "./components/FailureScreen";
import RetryButton from "./components/RetryButton";
import AnalyticsPage from "./components/AnalyticsPage";

const App = () => {
  const [step, setStep] = useState("pan");
  const [panData, setPANData] = useState(null);
  const [bankData, setBankData] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  const handlePANVerified = (data) => {
    setPANData(data);
    setStep("bank");
  };

  const handleBankAccountVerified = (data) => {
    setBankData(data);
    setStep("success");
  };

  const handleFailure = (message) => {
    setErrorMessage(message);
    setStep("failure");
  };

  const handleRetry = () => {
    setStep("pan");
    setPANData(null);
    setBankData(null);
    setErrorMessage("");
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <div>
            {step === "pan" && <VerificationModule onPANVerified={handlePANVerified} step="pan" />}
            {step === "bank" && (
              <VerificationModule
                onBankAccountVerified={handleBankAccountVerified}
                panData={panData}
                step="bank"
              />
            )}
            {step === "success" && <SuccessScreen panData={panData} bankData={bankData} />}
            {step === "failure" && (
              <FailureScreen errorMessage={errorMessage} onRetry={handleRetry} />
            )}
            {(step === "failure" || step === "success") && (
              <RetryButton onRetry={handleRetry} />
            )}
          </div>
        } />
        <Route path="/analytics" element={<AnalyticsPage />} />
      </Routes>
    </Router>
  );
};

export default App;

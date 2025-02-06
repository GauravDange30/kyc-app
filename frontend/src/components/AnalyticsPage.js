import React, { useEffect, useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";

const AnalyticsPage = () => {
  const [analyticsData, setAnalyticsData] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:8001/kyc_verification/api/analytics")
      .then((response) => {
        setAnalyticsData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching analytics data", error);
      });
  }, []);

  if (!analyticsData) return <p>Loading analytics...</p>;

  const chartData = {
    labels: analyticsData.labels, // Example: ["Success", "Failed"]
    datasets: [
      {
        label: "Verification Stats",
        data: analyticsData.values, // Example: [120, 30]
        backgroundColor: [
            "blue", // Total KYC Attempted
            "green", // Total KYC Successful
            "red", // Total KYC Failed
            "orange", // Failed Due to PAN
            "yellow", // Failed Due to Bank Account
            "purple", // Failed Due to PAN & Bank Account
          ],
      },
    ],
  };

  return (
    <div>
      <h2>Analytics Dashboard</h2>
      <Bar data={chartData} />
    </div>
  );
};

export default AnalyticsPage;

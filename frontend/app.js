const { useState } = React;

// API URL - use backend from Render or local
const API_URL = (() => {
  // If running on Render, use the Render backend URL
  if (window.location.hostname.includes('render.com')) {
    // Replace with your actual Render backend URL
    return 'https://claims-api.onrender.com';
  }
  // Otherwise use local development
  return 'http://127.0.0.1:5000';
})();

function App() {
  const [activeTab, setActiveTab] = useState("upload");
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  // Form state
  const [formData, setFormData] = useState({
    policy_number: "",
    policyholder_name: "",
    incident_date: "",
    incident_location: "",
    claim_type: "",
    estimated_damage: "",
    accident_description: "",
    vehicle_vin: "",
  });

  const handleFileChange = (event) => {
    setFile(event.target.files[0] || null);
    setError("");
    setResult(null);
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleFileSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setResult(null);

    if (!file) {
      setError("Please select a PDF or TXT file.");
      return;
    }

    const formPayload = new FormData();
    formPayload.append("file", file);

    try {
      setIsLoading(true);
      const response = await fetch(`${API_URL}/api/claims/process`, {
        method: "POST",
        body: formPayload,
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || "Request failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setIsLoading(false);
    }
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setResult(null);

    if (!formData.policy_number || !formData.policyholder_name) {
      setError("Please fill in required fields (marked with *)");
      return;
    }

    try {
      setIsLoading(true);
      const response = await fetch(`${API_URL}/api/claims/process-form`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || "Request failed");
      }

      const data = await response.json();
      setResult(data);
      setFormData({
        policy_number: "",
        policyholder_name: "",
        incident_date: "",
        incident_location: "",
        claim_type: "",
        estimated_damage: "",
        accident_description: "",
        vehicle_vin: "",
      });
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="header">
        <h1>Claims Processing</h1>
        <p>Upload a document or fill in details manually to process claims.</p>
      </header>

      <div className="tabs">
        <button
          className={`tab ${activeTab === "upload" ? "active" : ""}`}
          onClick={() => setActiveTab("upload")}
        >
          📄 Upload Document
        </button>
        <button
          className={`tab ${activeTab === "form" ? "active" : ""}`}
          onClick={() => setActiveTab("form")}
        >
          📝 Manual Entry
        </button>
      </div>

      {activeTab === "upload" && (
        <section className="card">
          <h2>Upload Claim Document</h2>
          <form onSubmit={handleFileSubmit}>
            <label className="file-input">
              <span>Select PDF or TXT</span>
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={handleFileChange}
              />
            </label>

            <button type="submit" disabled={isLoading}>
              {isLoading ? "Processing..." : "Process Claim"}
            </button>
          </form>

          {error && <div className="alert error">{error}</div>}
        </section>
      )}

      {activeTab === "form" && (
        <section className="card">
          <h2>Manual Claim Entry</h2>
          <form onSubmit={handleFormSubmit}>
            <div className="form-grid">
              <div className="form-group">
                <label>
                  Policy Number <span className="required">*</span>
                </label>
                <input
                  type="text"
                  name="policy_number"
                  value={formData.policy_number}
                  onChange={handleFormChange}
                  placeholder="e.g., POL-2024-001234"
                />
              </div>

              <div className="form-group">
                <label>
                  Policyholder Name <span className="required">*</span>
                </label>
                <input
                  type="text"
                  name="policyholder_name"
                  value={formData.policyholder_name}
                  onChange={handleFormChange}
                  placeholder="e.g., John Doe"
                />
              </div>

              <div className="form-group">
                <label>Incident Date</label>
                <input
                  type="date"
                  name="incident_date"
                  value={formData.incident_date}
                  onChange={handleFormChange}
                />
              </div>

              <div className="form-group">
                <label>Incident Location</label>
                <input
                  type="text"
                  name="incident_location"
                  value={formData.incident_location}
                  onChange={handleFormChange}
                  placeholder="e.g., Main Street, Springfield, IL"
                />
              </div>

              <div className="form-group">
                <label>Claim Type</label>
                <select
                  name="claim_type"
                  value={formData.claim_type}
                  onChange={handleFormChange}
                >
                  <option value="">Select claim type</option>
                  <option value="Auto Collision">Auto Collision</option>
                  <option value="Property Damage">Property Damage</option>
                  <option value="Bodily Injury">Bodily Injury</option>
                  <option value="Comprehensive">Comprehensive</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div className="form-group">
                <label>Estimated Damage ($)</label>
                <input
                  type="number"
                  name="estimated_damage"
                  value={formData.estimated_damage}
                  onChange={handleFormChange}
                  placeholder="e.g., 5000"
                />
              </div>

              <div className="form-group">
                <label>Vehicle VIN</label>
                <input
                  type="text"
                  name="vehicle_vin"
                  value={formData.vehicle_vin}
                  onChange={handleFormChange}
                  placeholder="e.g., 1HGBH41JXMN109186"
                />
              </div>

              <div className="form-group full-width">
                <label>Accident Description</label>
                <textarea
                  name="accident_description"
                  value={formData.accident_description}
                  onChange={handleFormChange}
                  placeholder="Describe what happened..."
                  rows="4"
                />
              </div>
            </div>

            <button type="submit" disabled={isLoading}>
              {isLoading ? "Processing..." : "Process Claim"}
            </button>
          </form>

          {error && <div className="alert error">{error}</div>}
        </section>
      )}

      {result && (
        <section className="card result">
          <h2>Processing Result</h2>
          <div className="result-summary">
            <div className="result-item">
              <span className="label">Route:</span>
              <span className="value">{result.recommendedRoute}</span>
            </div>
            <div className="result-item">
              <span className="label">Reasoning:</span>
              <span className="value">{result.reasoning}</span>
            </div>
            {result.missingFields && result.missingFields.length > 0 && (
              <div className="result-item">
                <span className="label">Missing Fields:</span>
                <span className="value">{result.missingFields.join(", ")}</span>
              </div>
            )}
            {result.fraudIndicators && result.fraudIndicators.length > 0 && (
              <div className="result-item alert-inline">
                <span className="label">⚠️ Fraud Indicators:</span>
                <span className="value">{result.fraudIndicators.join(", ")}</span>
              </div>
            )}
          </div>
          <details>
            <summary>Full JSON Response</summary>
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </details>
        </section>
      )}

      <footer className="footer">
        <p>Powered by Insurance Claims Processing Agent</p>
      </footer>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);

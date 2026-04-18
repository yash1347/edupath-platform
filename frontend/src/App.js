import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";

import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Opportunities from "./pages/Opportunities";
import AdminPanel from "./pages/AdminPanel";
import Chatbot from "./pages/Chatbot";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <Navbar />
        <div style={{ flex: 1 }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/opportunities" element={<Opportunities />} />
            <Route path="/admin" element={<AdminPanel />} />
            <Route path="/chat" element={<Chatbot />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

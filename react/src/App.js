import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Index from "./pages";
import Test from "./pages/test";
import NotFoundPage from "./pages/404";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/test-components" element={<Test />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
}

export default App;
